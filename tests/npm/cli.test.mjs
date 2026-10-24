import { test } from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { mkdtemp, readFile, readdir, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const exec = promisify(execFile);
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const CLI = path.join(ROOT, "bin", "agent-skills.mjs");

const run = (args) => exec(process.execPath, [CLI, ...args], { cwd: ROOT });

const pkg = JSON.parse(await readFile(path.join(ROOT, "package.json"), "utf8"));

test("list --json returns the pack catalog", async () => {
  const { stdout } = await run(["list", "--json"]);
  const data = JSON.parse(stdout);
  assert.equal(data.pack_version, pkg.version);
  assert.ok(data.skills.length >= 150, `expected a large catalog, got ${data.skills.length}`);
  for (const skill of data.skills) {
    assert.match(skill.name, /^[a-z0-9-]+$/);
    assert.ok(skill.source, `skill ${skill.name} has a source`);
  }
  assert.ok(data.skills.some((s) => s.name === "tune-game-feel" && s.taxonomy === "gamedev"));
  assert.ok(data.skills.some((s) => s.source !== "core"), "overlay skills are listed");
  assert.ok(data.roles.length >= 30);
  assert.ok(data.workflows.length >= 20);
});

test("list --taxonomy filters skills only", async () => {
  const { stdout } = await run(["list", "--json", "--taxonomy", "gamedev"]);
  const data = JSON.parse(stdout);
  assert.ok(data.skills.length >= 1);
  assert.ok(data.skills.every((s) => s.taxonomy === "gamedev"));
  assert.equal(data.roles.length, 0);
  assert.equal(data.workflows.length, 0);
});

test("install copies selected taxonomy into --path", async (t) => {
  const dest = await mkdtemp(path.join(tmpdir(), "agent-skills-"));
  t.after(() => rm(dest, { recursive: true, force: true }));

  const { stdout } = await run(["install", "--json", "--path", dest, "--taxonomy", "gamedev"]);
  const data = JSON.parse(stdout);
  assert.equal(data.target, dest);

  const listed = JSON.parse((await run(["list", "--json", "--taxonomy", "gamedev"])).stdout);
  assert.equal(data.installed.length, listed.skills.length);

  const onDisk = await readdir(dest, { withFileTypes: true });
  const dirs = onDisk.filter((e) => e.isDirectory());
  assert.equal(dirs.length, listed.skills.length);
  const tuneFeel = await readFile(path.join(dest, "tune-game-feel", "SKILL.md"), "utf8");
  assert.match(tuneFeel, /^---$/m);
});

test("install --skill copies exactly the named skills", async (t) => {
  const dest = await mkdtemp(path.join(tmpdir(), "agent-skills-"));
  t.after(() => rm(dest, { recursive: true, force: true }));

  const { stdout } = await run(["install", "--json", "--path", dest, "--skill", "tune-game-feel,write-use-cases"]);
  const data = JSON.parse(stdout);
  assert.deepEqual(
    data.installed.map((s) => s.name).sort(),
    ["tune-game-feel", "write-use-cases"]
  );
  const entries = await readdir(dest);
  assert.equal(entries.length, 2);
});

test("unknown skill names fail with exit 1", async () => {
  await assert.rejects(
    run(["install", "--path", "unused", "--skill", "no-such-skill"]),
    (error) => error.code === 1 && /no-such-skill/.test(error.stderr)
  );
});

test("missing destination is a usage error (exit 2)", async () => {
  await assert.rejects(run(["install"]), (error) => error.code === 2);
});
