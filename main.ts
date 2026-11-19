// Entry program for the make.fun bounty gta6-meme-x-01 (Node 22, standard library only).
// The entry itself is the meme post on X; POST.json carries that post's address.
// The grader reads /output/POST.json, so this program's whole job is to deliver
// the file there, byte for byte, and fail loudly if it cannot.
//
// Local trial (outside the grader's container):
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const sourceDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const entryFile = 'POST.json';

const sourcePath = join(sourceDir, entryFile);
const outputPath = join(outputDir, entryFile);

mkdirSync(outputDir, { recursive: true });
try {
  copyFileSync(sourcePath, outputPath);
} catch (problem) {
  console.error(`cannot deliver ${entryFile} from ${sourceDir}: ${(problem as Error).message}`);
  process.exit(1);
}

// Deterministic self-check: the delivered bytes must equal the source bytes.
if (!readFileSync(sourcePath).equals(readFileSync(outputPath))) {
  console.error(`${entryFile} copy differs from its source`);
  process.exit(1);
}
