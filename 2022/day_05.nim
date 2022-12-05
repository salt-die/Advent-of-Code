include aoc

let
  raw = fetch(2022, 5).split("\n\n").mapIt(it.splitLines)

  stacks = collect(for x in 0..8:
    collect(for y in 0..7:
      if raw[0][7 - y][1 + 4 * x] != ' ': raw[0][7 - y][1 + 4 * x]))

  commands = collect(for line in raw[1]:
    line.scanTuple("move $i from $i to $i"))

var mut_stacks: seq[seq[char]]
proc stack(i: int): var seq[char] = mut_stacks[i - 1]
proc stringify: string = collect(for s in mut_stacks: s[^1]).join("")

part 1:
  mut_stacks = stacks
  for (_, a, b, c) in commands:
    for _ in 0..<a:
      c.stack.add b.stack.pop
  stringify()

part 2:
  mut_stacks = stacks
  for (_, a, b, c) in commands:
    c.stack.add b.stack.toOpenArray(b.stack.len - a, b.stack.high)
    b.stack.setLen b.stack.len - a
  stringify()
