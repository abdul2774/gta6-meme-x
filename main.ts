// Entry program for make.fun's gta6-meme-x-01 bounty (Node 22+, standard
// library only). The real entry is the meme post on X; this program's single
// job is to hand the gate the repository's POST.json, which names that post.
// It copies POST.json from the repository root into the output directory,
// byte for byte, and does nothing else: no network, no clock, no state, so
// every run writes exactly the same bytes.
//
// The grader sets MAKEFUN_BOT_DIR (the repository) and MAKEFUN_OUTPUT_DIR
// (where POST.json must land). Locally:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const repoDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const source = join(repoDir, 'POST.json');
const target = join(outDir, 'POST.json');

if (!existsSync(source)) {
  console.error(`No POST.json found in the repository at ${source}`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(target, readFileSync(source));
