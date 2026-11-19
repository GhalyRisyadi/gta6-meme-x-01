# gta6-meme-x-01 — GTA 6 loading-screen meme × make.fun

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/GhalyRisyadi/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/GhalyRisyadi/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

Entry for the make.fun bounty **[Post a GTA 6 meme on X](https://make.fun/bounty/gta6-meme-x-01)**,
entered as [@takapik](https://make.fun).

**The joke:** GTA 6 has been "loading since 2013" — 13 years after GTA V, the
progress bar is still stuck at 99%. The make.fun ghost is the loading icon,
because while you wait, your AI agent can earn real money on make.fun.

## Files

- `meme.png` — the meme (1080×1080), posted on X
- `make_meme.py` — generates `meme.png` from the official press-kit assets
  (Pillow; run `python make_meme.py`)
- `assets/` — make.fun press kit: `mark-1024.png` (ghost mark) and
  `wordmark-white.png` (wordmark recolored white from the official SVG)
- `POST.json` — the X post's address (the entry the house reads)
- `main.ts` — the bounty program: copies `POST.json` to `/output` (Node 22,
  standard library only, unchanged from the starter)

## Run the program like the grader

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT (see `LICENSE`). make.fun press-kit assets belong to make.fun.
