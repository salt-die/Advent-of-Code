include std/prelude
import std/[heapqueue, re]

import nimpy

proc fetch*(year, day: int): string =
  # Get AoC input.
  "aoc_lube".pyImport.callMethod(string, "fetch", 2022, 1)

template part*(p: int, solution: untyped) =
  # Shortcut to print solution.
  echo "Part ", p, ": ", solution

proc extract_ints*(s: string): seq[int] =
  s.findAll(re"-?\d+").map(parseInt)

proc nlargest*[T](iterable: openArray[T], n: int): HeapQueue[T] =
  for i in iterable:
    if result.len < n:
      result.push i
    elif i > result[0]:
      discard result.replace i

template sum*(it: untyped): untyped =
  it.foldl(a + b)

template prod*(it: untyped): untyped =
  it.foldl(a * b)
