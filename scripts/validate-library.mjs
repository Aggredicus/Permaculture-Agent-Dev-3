import { promises as fs } from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";

const ROOT = process.cwd();
const errors = [];
const notes = [];

async function exists(p) {
  try { await fs.access(p); return true; } catch { return false; }
}

async function listDirs(relativeDir) {
  const absolute = path.join(ROOT, relativeDir);
  if (!(await exists(absolute))) return [];
  const entries = await fs.readdir(absolute, { withFileTypes: true });
  return entries.filter((entry) => entry.isDirectory()).map((entry) => entry.name).sort();
}

function frontmatter(text) {
  if (!text.startsWith("---\n")) return {};
  const end = text.indexOf("\n---\n", 4);
  if (end < 0) return {};
  const result = {};
  for (const line of text.slice(4, end).split("\n")) {
    const index = line.indexOf(":");
    if (index > 0) result[line.slice(0, index).trim()] = line.slice(index + 1).trim().replace(/^["']|["']$/g, "");
  }
  return result;
}

for (const skillName of await listDirs("skills")) {
  const base = path.join(ROOT, "skills", skillName);
  const skillPath = path.join(base, "SKILL.md");
  const versionPath = path.join(base, "VERSION");
  if (!(await exists(skillPath))) {
    errors.push(`${skillName}: missing SKILL.md`);
    continue;
  }
  if (!(await exists(versionPath))) {
    errors.push(`${skillName}: missing VERSION`);
    continue;
  }

  const skillText = await fs.readFile(skillPath, "utf8");
  const meta = frontmatter(skillText);
  if (meta.name !== skillName) errors.push(`${skillName}: frontmatter name must match folder`);
  if (!meta.description || meta.description.length < 40) errors.push(`${skillName}: description is missing or too vague`);

  const version = (await fs.readFile(versionPath, "utf8")).trim();
  if (!/^\d+\.\d+\.\d+$/.test(version)) errors.push(`${skillName}: VERSION must use semantic versioning`);

  const refs = [...skillText.matchAll(/`((?:references|assets|scripts)\/[A-Za-z0-9._/-]+)`/g)].map((match) => match[1]);
  for (const ref of refs) {
    if (!(await exists(path.join(base, ref)))) errors.push(`${skillName}: referenced path does not exist: ${ref}`);
  }

  if (/Aggredicus\/permaculture-works-website|dillonmichaellee\.workers\.dev/i.test(skillText)) {
    errors.push(`${skillName}: reusable SKILL.md contains project-specific repository or deployment values`);
  }

  notes.push(`${skillName}@${version}`);
}

const ontology = spawnSync(process.execPath, ["scripts/build-ontology.mjs", "--check"], { cwd: ROOT, encoding: "utf8" });
if (ontology.status !== 0) errors.push((ontology.stderr || ontology.stdout || "ontology check failed").trim());
else notes.push(ontology.stdout.trim());

if (errors.length) {
  for (const error of errors) console.error(`FAIL ${error}`);
  process.exitCode = 1;
} else {
  console.log(`Skill library valid: ${notes.join("; ")}`);
}
