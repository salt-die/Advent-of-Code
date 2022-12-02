include aoc

let
  strats = {
    'A': 0, 'B': 1, 'C': 2,
    'X': 0, 'Y': 1, 'Z': 2,
  }.toTable

  games = collect(
    for line in fetch(2022, 2).splitLines():
      (strats[line[0]], strats[line[2]])
  )

part 1: sum collect(for (a, b) in games: b + 1 + 3 * ((b - a + 1) % 3))
part 2: sum collect(for (a, b) in games: ((b - 1 + a) % 3) + 1 + 3 * b)