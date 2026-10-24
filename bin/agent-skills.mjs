#!/usr/bin/env node
/**
 * agent-skills — list and install skills from the @vesviet/agent-skills pack.
 * Exit codes follow the pack convention: 0 = pass, 1 = fail, 2 = usage error.
 */
import { access, cp, mkdir, readdir, readFile } from "node:fs/promises";
import { constants } from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const PKG_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const CORE_SKILLS = path.join(PKG_ROOT, "core", "skills");
const ROLES_DIR = path.join(PKG_ROOT, "core", "roles");
const WORKFLOWS_DIR = path.join(PKG_ROOT, "core", "workflows");
const OVERLAYS_DIR = path.join(PKG_ROOT, "overlays");

const INSTALL_TARGETS = {
  zcode: (home) => path.join(home, ".zcode", "skills"),
  claude: (home) => path.join(home, ".claude", "skills"),
  generic: () => path.join(process.cwd(), "agent-skills"),
};

const USAGE = `Usage: agent-skills <command> [options]

Commands:
  list      List skills, roles, and workflows in the pack
  install   Copy selected skills into an agent platform skills directory

Options:
  --taxonomy <a,b>   Filter by core taxonomy or overlay name
  --skill <a,b>      Select specific skills by slug
  --target <name>    Install destination: zcode | claude | generic
  --path <dir>       Install destination: explicit directory (overrides --target)
  --json             Machine-readable output
  --version          Print the pack version
  --help             Show this help

Examples:
  agent-skills list --taxonomy gamedev
  agent-skills install --target claude --taxonomy frontend,gamedev
  agent-skills install --path ./my-skills --skill tune-game-feel
`;

class UsageError extends Error {}

async function fileExists(target) {
  try {
    await access(target, constants.F_OK);
    return true;
  } catch {
    return false;
  }
}

async function packVersion() {
  const pkg = JSON.parse(await readFile(path.join(PKG_ROOT, "package.json"), "utf8"));
  return pkg.version;
}

async function listSkills() {
  const skills = [];
  for (const entry of await readdir(CORE_SKILLS, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const taxonomyDir = path.join(CORE_SKILLS, entry.name);
    for (const skill of await readdir(taxonomyDir, { withFileTypes: true })) {
      if (!skill.isDirectory()) continue;
      const dir = path.join(taxonomyDir, skill.name);
      if (!(await fileExists(path.join(dir, "SKILL.md")))) continue;
      skills.push({ name: skill.name, taxonomy: entry.name, source: "core", dir });
    }
  }
  for (const overlay of await readdir(OVERLAYS_DIR, { withFileTypes: true })) {
    if (!overlay.isDirectory()) continue;
    const skillsDir = path.join(OVERLAYS_DIR, overlay.name, "skills");
    if (!(await fileExists(skillsDir))) continue;
    for (const skill of await readdir(skillsDir, { withFileTypes: true })) {
      if (!skill.isDirectory()) continue;
      const dir = path.join(skillsDir, skill.name);
      if (!(await fileExists(path.join(dir, "SKILL.md")))) continue;
      skills.push({ name: skill.name, taxonomy: null, source: overlay.name, dir });
    }
  }
  return skills.sort((a, b) => a.name.localeCompare(b.name));
}

async function listMarkdown(dir, exclude) {
  if (!(await fileExists(dir))) return [];
  const entries = await readdir(dir, { withFileTypes: true });
  return entries
    .filter((e) => e.isFile() && e.name.endsWith(".md") && !exclude.includes(e.name))
    .map((e) => e.name.replace(/\.md$/, ""))
    .sort();
}

function parseArgs(argv) {
  const [command, ...rest] = argv;
  const flags = {};
  for (let i = 0; i < rest.length; i += 1) {
    const arg = rest[i];
    if (arg === "--json" || arg === "--help") {
      flags[arg] = true;
    } else if (["--taxonomy", "--skill", "--target", "--path"].includes(arg)) {
      const value = rest[i + 1];
      if (value === undefined || value.startsWith("--")) {
        throw new UsageError(`missing value for ${arg}`);
      }
      flags[arg] = value;
      i += 1;
    } else {
      throw new UsageError(`unknown argument: ${arg}`);
    }
  }
  return { command, flags };
}

function selectTaxonomies(flags) {
  if (!flags["--taxonomy"]) return null;
  return flags["--taxonomy"].split(",").map((t) => t.trim()).filter(Boolean);
}

async function cmdList(flags) {
  const taxonomies = selectTaxonomies(flags);
  const skills = (await listSkills()).filter(
    (s) => !taxonomies || taxonomies.includes(s.taxonomy) || taxonomies.includes(s.source)
  );
  const roles = taxonomies ? [] : await listMarkdown(ROLES_DIR, ["README", "role-standard"]);
  const workflows = taxonomies ? [] : await listMarkdown(WORKFLOWS_DIR, ["README"]);

  if (flags["--json"]) {
    process.stdout.write(
      JSON.stringify(
        { pack_version: await packVersion(), skills, roles, workflows },
        null,
        2
      ) + "\n"
    );
    return 0;
  }
  for (const s of skills) {
    process.stdout.write(`${s.name.padEnd(36)} ${s.taxonomy ?? `overlay/${s.source}`}\n`);
  }
  process.stdout.write(`\n${skills.length} skills, ${roles.length} roles, ${workflows.length} workflows\n`);
  return 0;
}

async function cmdInstall(flags) {
  if (!flags["--target"] && !flags["--path"]) {
    throw new UsageError("install requires --target (zcode | claude | generic) or --path <dir>");
  }
  let targetDir;
  if (flags["--path"]) {
    targetDir = path.resolve(flags["--path"]);
  } else {
    const resolver = INSTALL_TARGETS[flags["--target"]];
    if (!resolver) {
      throw new UsageError(`unknown --target '${flags["--target"]}' (valid: ${Object.keys(INSTALL_TARGETS).join(", ")})`);
    }
    targetDir = resolver(process.env.HOME ?? process.env.USERPROFILE);
  }

  const taxonomies = selectTaxonomies(flags);
  const wantedNames = flags["--skill"]
    ? flags["--skill"].split(",").map((s) => s.trim()).filter(Boolean)
    : null;
  const all = await listSkills();
  let selected = all.filter((s) => {
    if (s.source !== "core") return Boolean(wantedNames?.includes(s.name) || taxonomies?.includes(s.source));
    if (wantedNames && taxonomies) return wantedNames.includes(s.name) && taxonomies.includes(s.taxonomy);
    if (wantedNames) return wantedNames.includes(s.name);
    if (taxonomies) return taxonomies.includes(s.taxonomy);
    return true;
  });

  if (wantedNames) {
    const found = new Set(selected.map((s) => s.name));
    const missing = wantedNames.filter((n) => !found.has(n));
    if (missing.length > 0) {
      process.stderr.write(`Unknown skills: ${missing.join(", ")}\n`);
      return 1;
    }
  }
  if (selected.length === 0) {
    process.stderr.write("No skills matched the selection.\n");
    return 1;
  }

  await mkdir(targetDir, { recursive: true });
  for (const skill of selected) {
    await cp(skill.dir, path.join(targetDir, skill.name), { recursive: true, force: true });
  }

  if (flags["--json"]) {
    process.stdout.write(
      JSON.stringify(
        {
          pack_version: await packVersion(),
          target: targetDir,
          installed: selected.map((s) => ({ name: s.name, source: s.source === "core" ? s.taxonomy : `overlay/${s.source}` })),
        },
        null,
        2
      ) + "\n"
    );
  } else {
    process.stdout.write(`Installed ${selected.length} skills to ${targetDir}\n`);
    for (const s of selected) {
      process.stdout.write(`  ${s.name} (${s.source === "core" ? s.taxonomy : `overlay/${s.source}`})\n`);
    }
  }
  return 0;
}

async function main() {
  const { command, flags } = parseArgs(process.argv.slice(2));
  if (flags["--help"] || command === "help" || command === undefined) {
    process.stdout.write(USAGE);
    return command === undefined && !flags["--help"] ? 2 : 0;
  }
  if (flags["--version"] || command === "version") {
    process.stdout.write(`${await packVersion()}\n`);
    return 0;
  }
  if (command === "list") return cmdList(flags);
  if (command === "install") return cmdInstall(flags);
  throw new UsageError(`unknown command: ${command}`);
}

main()
  .then((code) => {
    process.exitCode = code;
  })
  .catch((error) => {
    if (error instanceof UsageError) {
      process.stderr.write(`${error.message}\n\n${USAGE}`);
      process.exitCode = 2;
    } else {
      process.stderr.write(`${error.stack ?? error}\n`);
      process.exitCode = 1;
    }
  });
