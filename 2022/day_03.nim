include aoc

type Sacks = seq[string] | seq[seq[char]]

let sacks = fetch(2022, 3).splitLines()

proc priority(c: char): int =
  1 + c.ord - (if c >= 'a': 'a'.ord else: 'A'.ord - 26)

proc sumPriorities(groups: seq[Sacks]): int =
  sum groups.mapIt(
    it.mapIt(it.toSet).foldl(a * b).chooseOne.priority
  )

part 1: sumPriorities sacks.mapIt(it.distribute(2))
part 2: sumPriorities sacks.chunk(3)