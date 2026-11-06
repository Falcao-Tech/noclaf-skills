"""Monta index.html com as cenas de src/, usando a duração real de cada narração."""
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAD, ERASE = 0.2, 0.6

STYLE = """
@font-face{font-family:"Caveat";src:url("assets/fonts/Caveat-700-latin.woff2") format("woff2");font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}
html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#f7f6f1}
#root{position:relative;width:100%;height:100%;overflow:hidden;background:#f7f6f1;font-family:"Caveat",cursive;font-weight:700;color:#20242b}
#frame{position:absolute;inset:12px;border:6px solid #cfd2d6;border-radius:14px;pointer-events:none;z-index:30}
.scene{position:absolute;inset:0;overflow:hidden}
.scene svg{position:absolute;inset:0;width:1920px;height:1080px;overflow:visible}
.under{z-index:1}.ink{z-index:2}.txt{position:absolute;inset:0;z-index:3}.er{z-index:9}
.t{position:absolute;line-height:1.02;white-space:nowrap;font-weight:700}
.note{position:absolute;background:#fff1a8;color:#20242b;padding:10px 20px;font:700 30px "IBM Plex Mono",Menlo,monospace;white-space:nowrap;box-shadow:2px 5px 8px rgba(32,36,43,.2)}
.note.hand{font-family:"Caveat",cursive;font-size:56px;line-height:1.05;padding:26px 34px}
.token{position:absolute;left:0;top:0;width:360px;height:180px;background:#ffe9e2;border:7px solid #c8381f;border-radius:10px;color:#c8381f;font-size:96px;line-height:166px;text-align:center;transform-origin:0 0}
#pen{position:absolute;left:0;top:0;width:150px;height:150px;z-index:20;overflow:visible;opacity:0}
"""

PEN = """<svg id="pen" viewBox="0 0 150 150"><g transform="rotate(-40)"><path d="M0 0 L10 -9 L10 9 Z" fill="#20242b"/><rect x="10" y="-13" width="26" height="26" fill="#7e8691"/><rect x="36" y="-16" width="110" height="32" rx="5" fill="#2f3a4a"/><rect x="146" y="-14" width="16" height="28" rx="3" fill="#c8381f"/></g></svg>"""


def norm(text):
    text = unicodedata.normalize("NFD", text.lower())
    return re.sub(r"[^a-z0-9]", "", text)


def read(path):
    return open(os.path.join(ROOT, path), encoding="utf-8").read()


def check_cues(code, scenes):
    """c.w anda só para a frente: uma palavra fora de ordem deixaria a animação fora de tempo."""
    parts = re.split(r'\n\s*"(\d\d)": function \(c\) \{', code)
    bodies = dict(zip(parts[1::2], parts[2::2]))
    errors = []
    for s in scenes:
        if s["id"] not in bodies:
            errors.append(f'cena {s["id"]} não existe em src/scenes.js')
            continue
        cursor = 0
        for cue in re.findall(r'c\.w\("([^"]+)"\)', bodies[s["id"]]):
            want = norm(cue)
            hit = next((i for i in range(cursor, len(s["words"])) if norm(s["words"][i]["w"]).startswith(want)), None)
            if hit is None:
                errors.append(f'cena {s["id"]}: "{cue}" não aparece na narração depois da marcação anterior')
            else:
                cursor = hit + 1
    return errors


def main():
    cfg = json.loads(read("video.json"))
    tail = cfg.get("tail", 0.5)
    ids = re.findall(r"^## (\d\d)\b", read("narration.md"), re.M)
    scenes, start = [], 0.0
    for sid in ids:
        data = json.loads(read(f"assets/voice/{sid}.words.json"))
        # O mp3 termina com silêncio: a cena acaba na última palavra, não no fim do arquivo.
        voice = round(data["words"][-1]["e"] + 0.15, 3)
        dur = round(LEAD + voice + tail + ERASE, 3)
        scenes.append({"id": sid, "start": round(start, 3), "duration": dur, "lead": LEAD, "voice": voice, "words": data["words"]})
        start += dur
    scenes[-1]["last"] = True
    total = round(start, 3)

    code = read("src/scenes.js")
    errors = check_cues(code, scenes)
    if errors:
        print("\n".join(errors))
        sys.exit(1)

    sections = "".join(
        f'<section id="s{s["id"]}" class="clip scene" data-start="{s["start"]}" data-duration="{s["duration"]}" data-track-index="1">'
        '<svg class="under" viewBox="0 0 1920 1080"></svg><svg class="ink" viewBox="0 0 1920 1080"></svg><div class="txt"></div><svg class="er" viewBox="0 0 1920 1080"></svg></section>'
        for s in scenes
    )
    audios = "".join(
        f'<audio id="a{s["id"]}" src="assets/voice/{s["id"]}.mp3" data-start="{round(s["start"] + LEAD, 3)}" data-duration="{s["voice"]}" data-track-index="2" data-volume="1"></audio>'
        for s in scenes
    )
    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<title>{cfg["title"]}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{STYLE}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
<div id="frame"></div>
{PEN}
{sections}
{audios}
</div>
<script>
{read("src/wb.js")}
{code}
var CFG = {json.dumps(scenes, ensure_ascii=False)};
document.fonts.load('700 48px Caveat').then(function () {{
  var tl = gsap.timeline({{ paused: true }});
  CFG.forEach(function (s) {{
    var c = makeScene(tl, s);
    SCENES[s.id](c);
    c.finish();
  }});
  tl.to({{}}, {{ duration: 0.001 }}, {total} - 0.001);
  window.__timelines["main"] = tl;
}});
</script>
</body>
</html>
"""
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"{len(scenes)} cenas, {total} s ({round(total / 60, 2)} min)")
    if "--words" in sys.argv:
        for s in scenes:
            print(f'cena {s["id"]} início {s["start"]}: ' + " ".join(f'{w["w"]}@{round(s["start"] + LEAD + w["s"], 1)}' for w in s["words"]))
    print("fim de cada cena (--at):", ",".join(str(round(s["start"] + s["duration"] - 0.75, 2)) for s in scenes))


main()
