include aoc

let
  raw = fetch(2022, 5).split("\n\n").mapIt(it.splitLines)

  stacks = collect(for x in 0..8:
    collect(for y in 0..7:
      if raw[0][7 - y][1 + 4 * x] != ' ': raw[0][7 - y][1 + 4 * x]))

  commands = collect(for line in raw[1]:
    line.scanTuple("move $i from $i to $i"))

part 1:
  var mut_stacks = stacks
  for (_, a, b, c) in commands:
    for _ in 0..<a:
      mut_stacks[c - 1].add mut_stacks[b - 1].pop

  collect(for stack in mut_stacks: stack[^1]).join("")

part 2:
  var giver: ptr seq[char]
  mut_stacks = stacks
  for (_, a, b, c) in commands:
    giver = addr mut_stacks[b - 1]
    for item in giver[^a..^1]:
      mut_stacks[c - 1].add item
    giver[].delete(giver[].len - a..<giver[].len)

  collect(for stack in mut_stacks: stack[^1]).join("")
