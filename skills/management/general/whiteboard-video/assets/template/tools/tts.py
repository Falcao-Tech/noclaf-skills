"""Grava a narração com o Edge TTS. A voz lê a grafia fonética; os tempos voltam com a palavra original.

Uso: tts.py          grava só as cenas cujo texto, voz ou pronúncia mudou
     tts.py --test [termos...]   grava review/teste-pronuncia.mp3 com os termos do dicionário
                                 usados na narração e os termos extras pedidos
"""
import asyncio
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata

import edge_tts

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE_DIR = os.path.join(ROOT, "assets", "voice")


def load(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return json.load(f)


CFG = load("video.json")
SAY = {**load("tools/pronuncia-base.json"), **load("pronuncia.json")}
SAY_LOWER = {k.lower(): v for k, v in SAY.items()}


def scenes():
    text = open(os.path.join(ROOT, "narration.md"), encoding="utf-8").read()
    found = re.findall(r"^## (\d\d)\b.*\n+((?:(?!^## ).*\n?)+)", text, re.M)
    return [(sid, " ".join(body.split())) for sid, body in found]


def norm(text):
    text = unicodedata.normalize("NFD", text.lower())
    return re.sub(r"[^a-z0-9]", "", text)


def core(token):
    match = re.match(r"^([^\w]*)([\w#-]+?)([^\w]*)$", token)
    return match.groups() if match else ("", token, "")


def spoken_tokens(text):
    out = []
    for token in text.split():
        before, word, after = core(token)
        say = SAY.get(word) or SAY_LOWER.get(word.lower())
        out.append((token, before + say + after if say else token))
    return out


def align(tokens, marks):
    """Um token pode virar várias palavras faladas; agrupa as marcas de volta na palavra original."""
    words, i = [], 0
    for original, spoken in tokens:
        want, got, first, last = len(norm(spoken)), 0, None, None
        if not want:
            continue
        while i < len(marks) and got < want:
            first = first or marks[i]
            last = marks[i]
            got += len(norm(marks[i]["text"]))
            i += 1
        first, last = first or marks[-1], last or marks[-1]
        words.append({"w": original, "s": round(first["offset"] / 1e7, 3), "e": round((last["offset"] + last["duration"]) / 1e7, 3)})
    return words


def media_duration(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]))


async def synth(sid, text):
    mp3, meta = os.path.join(VOICE_DIR, f"{sid}.mp3"), os.path.join(VOICE_DIR, f"{sid}.words.json")
    tokens = spoken_tokens(text)
    spoken = " ".join(s for _, s in tokens)
    key = hashlib.sha1(f'{CFG["voice"]}|{CFG["rate"]}|{spoken}'.encode()).hexdigest()
    if os.path.exists(meta) and json.load(open(meta, encoding="utf-8")).get("key") == key:
        return sid, "sem mudança"
    comm = edge_tts.Communicate(spoken, CFG["voice"], rate=CFG["rate"], boundary="WordBoundary")
    audio, marks = bytearray(), []
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            audio.extend(chunk["data"])
        elif chunk["type"] == "WordBoundary":
            marks.append(chunk)
    with open(mp3, "wb") as f:
        f.write(audio)
    data = {"key": key, "duration": round(media_duration(mp3), 3), "words": align(tokens, marks)}
    with open(meta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return sid, data["duration"]


async def pronunciation_test():
    words = {core(t)[1].lower() for _, text in scenes() for t in text.split()}
    used = [(k, v) for k, v in SAY.items() if k.lower() in words]
    used += [(a, SAY_LOWER.get(a.lower(), a)) for a in sys.argv[2:]]
    os.makedirs(os.path.join(ROOT, "review"), exist_ok=True)
    out = os.path.join(ROOT, "review", "teste-pronuncia.mp3")
    await edge_tts.Communicate(". ".join(v for _, v in used) + ".", CFG["voice"], rate=CFG["rate"]).save(out)
    print(out, round(media_duration(out), 1), "s")
    for k, v in used:
        print(f"{k}: {v}")


async def main():
    if "--test" in sys.argv:
        await pronunciation_test()
        return
    os.makedirs(VOICE_DIR, exist_ok=True)
    for sid, text in scenes():
        print(await synth(sid, text))


asyncio.run(main())
