include aoc

let raw = fetch(2022, 6)

proc unique(n: int): int =
  var s: set[char] = {}

  s.symAdd raw.toOpenArray(0, n - 1)
  for i in n..raw.high:
    if s.len == n:
      return i
    s.symAdd(raw[i - n], raw[i])

part 1: unique 4
part 2: unique 14