include aoc
import fusion/matching
{.experimental: "caseStmtMacros".}

type Path = ref object
  directories: Table[string, Path]
  files: Table[string, int]
  parent: Path

proc size(path: Path): int =
  path.files.values.toSeq.sum + path.directories.values.toSeq.mapIt(it.size).sum

iterator iter_dir(path: Path): Path {.closure.} =
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