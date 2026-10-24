#!/usr/bin/env node
/** Fails when package.json drifts from VERSION so `npm publish` cannot ship a stale version. */
import { readFile } from "node:fs/promises";
import process from "node:process";

const read = (p) => readFile(new URL(p, import.meta.url), "utf8");

const version = (await read("../VERSION")).trim();
const pkg = JSON.parse(await read("../package.json"));

if (pkg.version !== version) {
  process.stderr.write(`package.json version ${pkg.version} != VERSION ${version}\n`);
  process.exit(1);
}
process.stdout.write(`npm version sync OK: ${version}\n`);
