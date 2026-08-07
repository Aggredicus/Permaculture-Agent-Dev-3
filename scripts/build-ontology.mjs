import { promises as fs } from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const ROOT = process.cwd();
const CONFIG_PATH = "ontology/ontology.config.json";
const SEMANTICS_PATH = "ontology/semantics.json";
const OUT_JSON = "ontology/SELF_MODEL.json";
const OUT_GRAPHML = "ontology/SELF_MODEL.graphml";

const config = JSON.parse(await fs.readFile(path.join(ROOT, CONFIG_PATH), "utf8"));
const semantics = JSON.parse(await fs.readFile(path.join(ROOT, SEMANTICS_PATH), "utf8"));
const excluded = new Set(config.exclude ?? []);

async function exists(rel) {
  try { await fs.access(path.join(ROOT, rel)); return true; } catch { return false; }
}

async function walk(dir) {
  if (!(await exists(dir))) return [];
  const entries = await fs.readdir(path.join(ROOT, dir), { withFileTypes: true });
  const out = [];
  for (const entry of entries.sort((a, b) => a.name.localeCompare(b.name))) {
    const rel = path.posix.join(dir, entry.name);
    if (excluded.has(rel)) continue;
    if (entry.isDirectory()) out.push(...await walk(rel));
    else if (entry.isFile()) out.push(rel);
  }
  return out;
}

function kind(file) {
  if (file.startsWith("skills/")) return "skill-file";
  if (file.startsWith(".github/workflows/")) return "workflow";
  if (file.startsWith("scripts/")) return "script";
  if (file.startsWith("ontology/")) return "ontology-source";
  if (file.startsWith("docs/")) return "documentation";
  if (file === "AGENTS.md") return "repository-instructions";
  if (file === "README.md") return "documentation";
  return "file";
}

const files = new Set();
for (const file of config.rootFiles ?? []) if (await exists(file) && !excluded.has(file)) files.add(file);
for (const dir of config.scanRoots ?? []) for (const file of await walk(dir)) files.add(file);

const nodes = new Map([["repo", ["repo", "repository", config.rootLabel]]]);
const edges = [];

const skillNames = [...new Set([...files].filter((f) => f.startsWith("skills/")).map((f) => f.split("/")[1]))].sort();
for (const name of skillNames) {
  const id = `skill:${name}`;
  nodes.set(id, [id, "skill"]);
  edges.push(["repo", "contains", id]);
}

for (const file of [...files].sort()) {
  const id = `file:${file}`;
  nodes.set(id, [id, kind(file)]);
  if (file.startsWith("skills/")) edges.push([`skill:${file.split("/")[1]}`, "contains", id]);
  else edges.push(["repo", "contains", id]);
}

for (const node of semantics.nodes ?? []) {
  if (!Array.isArray(node) || node.length < 2) throw new Error("Invalid semantic node");
  nodes.set(node[0], node);
}
for (const edge of semantics.edges ?? []) {
  if (!Array.isArray(edge) || edge.length !== 3) throw new Error("Invalid semantic edge");
  edges.push(edge);
}

const nodeList = [...nodes.values()].sort((a, b) => a[0].localeCompare(b[0]));
const edgeList = edges
  .filter((edge, i, all) => all.findIndex((x) => x.join("\0") === edge.join("\0")) === i)
  .sort((a, b) => a.join("\0").localeCompare(b.join("\0")));

const ids = new Set(nodeList.map((node) => node[0]));
for (const [from, , to] of edgeList) if (!ids.has(from) || !ids.has(to)) throw new Error(`Dangling edge: ${from} -> ${to}`);

const fingerprint = crypto.createHash("sha256").update(JSON.stringify([nodeList, edgeList])).digest("hex").slice(0, 20);
const model = { v: 1, model: config.modelName, repository: config.repository, fingerprint, nodes: nodeList, edges: edgeList };
const jsonText = `${JSON.stringify(model)}\n`;

function xml(v) {
  return String(v).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&apos;");
}
function graphLabel(node) {
  const [id, , label] = node;
  if (label) return label;
  if (id.startsWith("file:")) return id.slice(5).split("/").at(-1);
  if (id.startsWith("skill:")) return id.slice(6);
  return id;
}
function graphPath(node) {
  const id = node[0];
  if (id.startsWith("file:")) return id.slice(5);
  if (id.startsWith("skill:")) return `skills/${id.slice(6)}`;
  return node[3] ?? "";
}

const graphNodes = nodeList.map((node) => {
  const [id, nodeKind] = node;
  const p = graphPath(node);
  return `    <node id="${xml(id)}"><data key="kind">${xml(nodeKind)}</data><data key="label">${xml(graphLabel(node))}</data>${p ? `<data key="path">${xml(p)}</data>` : ""}</node>`;
}).join("\n");
const graphEdges = edgeList.map(([from, relation, to], i) =>
  `    <edge id="e${i + 1}" source="${xml(from)}" target="${xml(to)}"><data key="relation">${xml(relation)}</data></edge>`
).join("\n");
const graphmlText = `<?xml version="1.0" encoding="UTF-8"?>\n<graphml xmlns="http://graphml.graphdrawing.org/xmlns">\n  <key id="kind" for="node" attr.name="kind" attr.type="string"/>\n  <key id="label" for="node" attr.name="label" attr.type="string"/>\n  <key id="path" for="node" attr.name="path" attr.type="string"/>\n  <key id="relation" for="edge" attr.name="relation" attr.type="string"/>\n  <key id="fingerprint" for="graph" attr.name="fingerprint" attr.type="string"/>\n  <graph id="${xml(config.modelName)}" edgedefault="directed">\n    <data key="fingerprint">${fingerprint}</data>\n${graphNodes}\n${graphEdges}\n  </graph>\n</graphml>\n`;

async function same(rel, expected) {
  if (!(await exists(rel))) return false;
  return (await fs.readFile(path.join(ROOT, rel), "utf8")) === expected;
}

if (process.argv.includes("--write")) {
  await fs.writeFile(path.join(ROOT, OUT_JSON), jsonText);
  await fs.writeFile(path.join(ROOT, OUT_GRAPHML), graphmlText);
  console.log(`Wrote ${config.modelName}: ${nodeList.length} nodes, ${edgeList.length} edges, ${fingerprint}`);
} else {
  if (!(await same(OUT_JSON, jsonText)) || !(await same(OUT_GRAPHML, graphmlText))) {
    console.error("Ontology is stale. Run: node scripts/build-ontology.mjs --write");
    process.exitCode = 1;
  } else {
    console.log(`Ontology current: ${nodeList.length} nodes, ${edgeList.length} edges, ${fingerprint}`);
  }
}
