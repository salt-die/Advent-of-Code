include aoc

let RANGES = collect(for line in fetch(2022, 4).splitLines:
  line.scanTuple("$i-$i,$i-$i")
)

part 1: sum collect(
  for (_, a, b, c, d) in RANGES:
    int a <= c and d <= b or c <= a and b <= d
)

part 2: sum collect(
  for (_, a, b, c, d) in RANGES:
    int a <= d and c <= b
)