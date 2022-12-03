include aoc

let sacks = fetch(2022, 3).splitLines()

proc priority(letter: char): int =
  let offset = letter.isLowerAscii ? 'a'.ord: 'A'.ord - 26
  1 + letter.ord - offset

part 1: sum sacks
  .mapIt(
    it
    .toSeq
    .distribute(2)
    .mapIt(it.toHashSet)
    .foldl(a * b)
    .pop
    .priority
  )

part 2: sum sacks
  .distribute(sacks.len div 3)
  .mapIt(
    it
    .mapIt(it.toHashSet)
    .foldl(a * b)
    .pop
    .priority
  )