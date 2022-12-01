import std/[algorithm, re, sequtils, strutils, sugar]
import nimpy

proc extract_ints(s: string): seq[int] =
  collect(for i in s.findAll(re"-?\d+"): i.parseInt)

let
  aoc_lube = nimpy.pyImport("aoc_lube")
  RAW = nimpy.callMethod(aoc_lube, string, "fetch", 2022, 1).split("\n\n")
  CALORIES = collect(for elf in RAW: extract_ints(elf).foldl(a + b))

echo "Part 1: ", CALORIES.max
echo "Part 2: ", CALORIES.sorted(cmp[int], order=SortOrder.Descending)[..2].foldl(a + b)