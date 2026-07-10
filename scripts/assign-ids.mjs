#!/usr/bin/env node
// Atribui ids SEQUENCIAIS estáveis no frontmatter de cada item da vault
// (commands/*.md, skills/**/SKILL.md, agents/*.md). Ids existentes NUNCA mudam —
// só docs sem `id:` recebem o próximo número. É a chave estável de telemetria que
// sobrevive a renames. Rode: `node scripts/assign-ids.mjs` (ou `npm run ids`).
import { readdirSync, readFileSync, writeFileSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const KINDS = ["commands", "skills", "agents"];

function walk(dir, out = []) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith(".")) continue;
    const p = join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.isFile() && e.name.toLowerCase().endsWith(".md")) out.push(p);
  }
  return out;
}

/** É um "item" (vira skill/command/agent)? READMEs e arquivos de apoio não são. */
function isItem(rel) {
  const parts = rel.split("/");
  const base = parts[parts.length - 1].toLowerCase();
  if (base === "readme.md") return false;
  const kind = parts[0];
  if (kind === "commands" || kind === "agents") return true;
  if (kind === "skills") return base === "skill.md";
  return false;
}

function frontmatter(raw) {
  const m = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/.exec(raw);
  return m ? { block: m[0], inner: m[1], body: raw.slice(m[0].length) } : null;
}

function readId(inner) {
  const m = /^id:\s*(.+)$/m.exec(inner);
  return m ? m[1].trim().replace(/^["']|["']$/g, "") : null;
}

// 1) coleta os items + ids existentes
const files = [];
for (const kind of KINDS) {
  const dir = join(ROOT, kind);
  try {
    statSync(dir);
  } catch {
    continue;
  }
  for (const abs of walk(dir)) {
    const rel = abs.slice(ROOT.length + 1).split(/[\\/]/).join("/");
    if (!isItem(rel)) continue;
    const raw = readFileSync(abs, "utf8");
    const fm = frontmatter(raw);
    files.push({ abs, rel, raw, fm, id: fm ? readId(fm.inner) : null });
  }
}

// 2) valida unicidade dos ids existentes
const used = new Set();
let dup = false;
for (const f of files) {
  if (f.id == null) continue;
  if (used.has(f.id)) {
    console.error(`✗ id duplicado: ${f.id} (${f.rel})`);
    dup = true;
  }
  used.add(f.id);
}
if (dup) {
  console.error("Corrija os ids duplicados antes de continuar.");
  process.exit(1);
}

// 3) próximo id = max(contador persistido, maior existente + 1). O contador em
//    `.noclaf-ids.json` garante que ids deletados NUNCA são reusados (histórico
//    de telemetria fica sem ambiguidade).
const SEQ_FILE = join(ROOT, ".noclaf-ids.json");
let persisted = 0;
try {
  persisted = Number(JSON.parse(readFileSync(SEQ_FILE, "utf8")).next) || 0;
} catch {
  /* primeira vez */
}
const nums = [...used].map(Number).filter((n) => Number.isInteger(n));
let next = Math.max(persisted, nums.length ? Math.max(...nums) + 1 : 1);
const startNext = next;

// 4) atribui aos sem-id (ordem estável por path), mantendo os existentes
let assigned = 0;
for (const f of files.filter((x) => x.id == null).sort((a, b) => a.rel.localeCompare(b.rel))) {
  const id = String(next++);
  const out = f.fm
    ? `---\nid: ${id}\n${f.fm.inner}\n---\n${f.fm.body}`
    : `---\nid: ${id}\n---\n\n${f.raw}`;
  writeFileSync(f.abs, out, "utf8");
  console.log(`+ id ${id} → ${f.rel}`);
  assigned++;
}

// 5) persiste o contador (monotônico — nunca reusa ids deletados)
if (next !== startNext || persisted === 0) {
  writeFileSync(SEQ_FILE, JSON.stringify({ next }, null, 2) + "\n", "utf8");
}

console.log(
  assigned
    ? `\n${assigned} ids atribuídos · ${files.length} items · próximo id: ${next}`
    : `Todos os ${files.length} items já têm id (próximo: ${next}).`,
);
