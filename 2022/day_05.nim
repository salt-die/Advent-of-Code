include aoc

let
  raw = fetch(2022, 5).split("\n\n").mapIt(it.splitLines)

  stacks = collect(for x in 0..8:
    collect(for y in 0..7:
      if raw[0][7 - y][1 + 4 * x] != ' ': raw[0][7 - y][1 + 4 * x]))

  commands = collect(for line in raw[1]:
    line.scanTuple("move $i from $i to $i"))

var mut_stacks: seq[seq[char]]
template stack_b: auto = mut_stacks[b - 1]
template stack_c: auto = mut_stacks[c - 1]

part 1:
  mut_stacks = stacks
  for (_, a, b, c) in commands:
    for _ in 0..<a:
      stack_c.add stack_b.pop
  collect(for stack in mut_stacks: stack[^1]).join("")

part 2:
  mut_stacks = stacks
  for (_, a, b, c) in commands:
    for item in stack_b[^a..^1]:
      stack_c.add item
    stack_b.setLen(stack_b.len - a)

  collect(for stack in mut_stacks: stack[^1]).join("")
