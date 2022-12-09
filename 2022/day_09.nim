include aoc
import std/sets

type vec2 = array[2, int]

let commands = block:
  var commands: seq[(vec2, int)]

  proc toDelta(dir: char): vec2 =
    case dir:
    of 'U': [0, 1]
    of 'D': [0, -1]
    of 'L': [-1, 0]
    else: [1, 0]

  for line in fetch(2022, 9).splitlines():
    let (_, dir, n) = line.scanTuple("$c $i")
    commands.add (dir.toDelta, n)

  commands

using a, b: vec2

proc `+=`(a: var vec2, b) =
  a[0] += b[0]
  a[1] += b[1]

proc `-`(a, b): vec2 = [a[0] - b[0], a[1] - b[1]]

proc sign(n: int): int =
  if n > 0: 1 elif n < 0: -1 else: 0

proc sign(a): vec2 = [a[0].sign, a[1].sign]

proc chebyshev(a): int = max(a[0].abs, a[1].abs)

proc simulate_rope(nknots: int): int =
  var
    rope = collect(for _ in 0..<nknots: [0, 0])
    seen = toHashSet [[0, 0]]

  for (dir, n) in commands:
    for _ in 0..<n:
      rope[0] += dir
      for i in 0..<nknots - 1:
        let delta = rope[i] - rope[i + 1]
        if delta.chebyshev > 1: rope[i + 1] += delta.sign
      seen.incl rope[^1]

  seen.len

part 1: simulate_rope 2
part 2: simulate_rope 10