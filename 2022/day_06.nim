include aoc

let raw = fetch(2022, 6)

proc unique(n: int): int =
  for i in n..raw.high:
    if raw.toOpenArray(i, i + n - 1).toSet.len == n:
      return i + n

part 1: unique 4
part 2: unique 14