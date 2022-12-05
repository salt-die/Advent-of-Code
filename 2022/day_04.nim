include aoc

let RANGES = block:
  var a, b, c, d: int
  collect(
    for line in fetch(2022, 4).splitLines:
      discard line.scanf("$i-$i,$i-$i", a, b, c, d)
      (a, b, c, d)
  )

part 1: sum collect(
  for (a, b, c, d) in RANGES:
    int a <= c and d <= b or c <= a and b <= d
)

part 2: sum collect(
  for (a, b, c, d) in RANGES:
    int a <= d and c <= b
)