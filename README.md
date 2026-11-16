# tiny-chess-01

[![make.fun](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/highwill/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/highwill/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01)

The strongest chess engine I could fit in 4,096 bytes of Python, built for
[make.fun's tiny-chess-01](https://make.fun/bounty/tiny-chess-01): one game
after another against a fixed gauntlet of eight house engines, rated by Elo.

## The engine

`main.py` is the whole engine (packed from `engine.py` with
`makefun compress`, LZMA + stub). 0x88 board, negamax alpha-beta with
iterative deepening to a fixed node budget, quiescence on captures,
MVV-LVA + killer + history move ordering, a transposition table, and a
material + piece-square evaluation with an endgame king blend.

- Deterministic: search to a fixed node count, never a clock, no
  unseeded randomness, so a replay plays the same moves.
- No model calls, no network but the env, standard library only.
- About 40,000 nodes a move, ~1 second on one CPU.

## Size rule

- `main.py` is the whole engine: at most 4,096 bytes as committed.
- The rest of the tree (this README, LICENSE) is at most 8,192 bytes
  in all, and no file over 4,096.

## Grade it locally

From inside the competition's dev kit:

    makefun grade-local --kit . --bot <this repository> --driver docker

It plays one practice trial against the house engines, replays it, and
prints the Elo the scorer gives it.
