[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/abdul2774/gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/abdul2774/gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

# Jason & Lucia Receipt — a GTA 6 meme for make.fun

An original GTA 6 meme, "Jason & Lucia Receipt" — a fan's itemized waiting bill for Grand Theft Auto VI — posted on X: https://x.com/Bitcoin2Earn/status/2124768074016653662

This repository is the entry for make.fun's gta6-meme-x-01 bounty ("Post a GTA 6 meme on X"): https://make.fun/bounty/gta6-meme-x-01

The meme lives in `meme/`, `POST.json` at the root names the post's address, and `main.ts` (Node 22) simply copies `POST.json` into the output directory — the post itself, read from X, is what gets judged.

## Run

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
