import std/[heapqueue, sequtils, strutils, sugar]
import nimpy

template sum(sequence: untyped): untyped =
  sequence.foldl(a + b)

proc nlargest[T](iterable: openArray[T], n: int): HeapQueue[T] =
  for i in iterable:
    if result.len < n:
      result.push i
    elif i > result[0]:
      discard result.replace i

let
  RAW = "aoc_lube".pyImport.callMethod(string, "fetch", 2022, 1).split("\n\n")
  CALORIES = collect(for elf in RAW: elf.split.map(parseInt).sum)

echo "Part 1: ", CALORIES.max
echo "Part 2: ", CALORIES.nlargest(3).sum