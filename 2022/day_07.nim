include aoc
import fusion/matching
{.experimental: "caseStmtMacros".}

type Path = ref object
  directories: Table[string, Path]
  files: Table[string, int]
  parent: Path

proc size(path: Path): int =
  path.files.values.toSeq.sum + path.directories.values.toSeq.mapIt(it.size).sum

iterator iter_dir(path: Path): Path =
  var stack = @[path]

  while stack.len > 0:
    let cwd = stack.pop()
    yield cwd
    for name, path in cwd.directories:
      stack.add path

var system = Path()

block:
  var cwd = system
  system.directories["/"] = Path()

  for line in fetch(2022, 7).splitlines.mapIt(it.split):
    case line:
      of ["$", "cd", ".."]:
        cwd = cwd.parent
      of ["$", "cd", @dir]:
        cwd = cwd.directories[dir]
      of ["$", "ls"]:
        discard
      of ["dir", @dir]:
        if dir notin cwd.directories:
          cwd.directories[dir] = Path(parent: cwd)
      of [@size, @file]:
          cwd.files[file] = size.parseInt

part 1:
  sum collect(for dir in system.iter_dir:
    let size = dir.size
    if size <= 100_000: size
  )

part 2:
  let needed = system.size - 40_000_000
  collect(for dir in system.iter_dir:
    let size = dir.size
    if size > needed: size
  ).min

## Alternative fast solution:
# let sizes = block:
#   var sizes, stack: seq[int]

#   proc stack_pop =
#     sizes.add stack.pop
#     if stack.len > 0:
#       stack[^1] += sizes[^1]

#   for line in fetch(2022, 7).splitlines.mapIt(it.split):
#     case line:
#       of ["$", "cd", ".."]: stack_pop()
#       of ["$", "cd", _]: stack.add 0
#       of ["$", "ls"]: discard
#       of ["dir", _]: discard
#       of [@size, _]: stack[^1] += size.parseInt

#   while stack.len > 0: stack_pop()

#   sizes

# part 1: sum sizes.filterIt(it <= 100_000)

# part 2: min sizes.filterIt(it > sizes[^1] - 40_000_000)
