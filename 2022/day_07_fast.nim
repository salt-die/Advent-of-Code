include aoc
import fusion/matching
{.experimental: "caseStmtMacros".}

let sizes = block:
  var sizes, stack: seq[int]

  proc stack_pop =
    sizes.add stack.pop
    stack[^1] += sizes[^1]

  for line in fetch(2022, 7).splitlines.mapIt(it.split):
    case line:
    of ["$", "cd", ".."]: stack_pop()
    of ["$", "cd", _]: stack.add 0
    of ["$", "ls"]: discard
    of ["dir", _]: discard
    of [@size, _]: stack[^1] += size.parseInt

  while stack.len > 1: stack_pop()
  sizes.add stack
  sizes

part 1: sum sizes.filterIt(it <= 100_000)

part 2: min sizes.filterIt(it > sizes[^1] - 40_000_000)