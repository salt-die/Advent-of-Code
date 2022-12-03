include std/prelude
import std/[heapqueue, math, re, sugar]

import nimpy

proc fetch*(year, day: int): string =
  ## Get AoC input.
  "aoc_lube".pyImport.callMethod(string, "fetch", year, day)

template part*(p: int, solution: untyped) =
  ## Template to print solution.
  echo "Part ", p, ": ", solution

proc extract_ints*(s: string): seq[int] =
  ## Extract all integers from a string.
  s.findAll(re"-?\d+").map(parseInt)

proc nlargest*[T](iterable: openArray[T], n: int): HeapQueue[T] =
  ## Return n largest items from iterable.
  for i in iterable:
    if result.len < n:
      result.push i
    elif i > result[0]:
      discard result.replace i

proc `%`*(a, b: int): int =
  floorMod(a, b)

template sum*(it: untyped): untyped =
  ## Sum of all items in iterable.
  it.foldl(a + b)

template prod*(it: untyped): untyped =
  ## Product of all items in iterable.
  it.foldl(a * b)

template `?`*(cond: bool; a, b: untyped): untyped =
  if cond:
    a
  else:
    b