include aoc

let RANGES = fetch(2022, 4).findAll(re"\d+").map(parseInt).chunk(4)

part 1: sum collect(
  for r in RANGES:
    (a, b, c, d) =* r
    int a <= c and d <= b or c <= a and b <= d
)

part 2: sum collect(
  for r in RANGES:
    (a, b, c, d) =* r
    int a <= d and c <= b
)