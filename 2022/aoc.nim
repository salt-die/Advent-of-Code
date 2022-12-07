import std/[heapqueue, macros, math, parseopt, parseutils, re, sequtils,
            setutils, strformat, strscans, strutils, sugar, tables]

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

template sum*(it: untyped): int =
  ## Sum of all items in iterable.
  it.foldl(a + b, 0)

template prod*(it: untyped): int =
  ## Product of all items in iterable.
  it.foldl(a * b, 1)

proc distribute*(it: string, n: Positive, spread: bool=false): seq[seq[char]] =
  ## Distribute for strings.
  it.toSeq.distribute(n, spread)

template chunk*(it: untyped, n: int): untyped =
  ## Chunk iterable into groups of `n`.
  it.distribute(it.len div n)

proc chooseOne*[T](s: set[T]): T =
  for x in s: return x

macro `=*`*(lhs, rhs: untyped): auto =
  ## Unpacking macro.
  result = newStmtList()
  for i, v in lhs:
    result.add(
      quote do:
        let `v` = `rhs`[`i`]
    )

proc symAdd*[T](s: var set[T], items: varargs[T]) =
  ## Add an item if not in the set, else remove it.
  for item in items:
    if item in s:
      s.excl item
    else:
      s.incl item
