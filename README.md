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
iterative deepening to a fixed node budget, quiescence on captures
(with mate detection when in check), MVV-LVA + killer + history move
ordering, late-move reductions, null-move pruning, a transposition
table, repetition scoring 0 inside the search, and a material +
piece-square evaluation with passed-pawn, pawn-structure and bishop-pair
terms and an endgame king blend.

Round 2 (this commit): passed-pawn test inlined over the pawn lists,
quiescence captures sorted by MVV-LVA, the root keeps its partial best
when the node budget runs out, node budget 140,000, null-move reduction
2, late-move reductions from the 3rd move on. Practice Elo 1,467 over
six trials (round 1: 1,365), beating the house baseline's 1,365.

- Deterministic: search to a fixed node count, never a clock, no
  unseeded randomness, so a replay plays the same moves.
- No model calls, no network but the env, standard library only.
- About 140,000 nodes a move, ~3-4 seconds on one CPU.

## Size rule

- `main.py` is the whole engine: at most 4,096 bytes as committed.
- The rest of the tree (this README, LICENSE) is at most 8,192 bytes
  in all, and no file over 4,096.

## Grade it locally

From inside the competition's dev kit:

    makefun grade-local --kit . --bot <this repository> --driver docker

It plays one practice trial against the house engines, replays it, and
prints the Elo the scorer gives it.
