import std/[heapqueue, sets, strutils, enumerate, sugar, tables, sequtils]
import nimpy

proc fetch(year, day: int): string = "aoc_lube".pyImport.callMethod(string, "fetch", year, day)

type 
  Vec2 = tuple[y: int, x: int]
  State = tuple[score: int, pos: Vec2, dir: Vec2, seats: seq[Vec2]]

proc `+`(a, b: Vec2): Vec2 = (a.y + b.y, a.x + b.x)
proc `-`(a, b: Vec2): Vec2 = (a.y - b.y, a.x - b.x)
proc `<`(a, b: State): bool = a.score < b.score

let 
  MAZE = collect:
    for y, line in enumerate fetch(2024, 16).splitLines:
      for x, chr in enumerate line:
        if chr != '#': {(y, x)}
  START = (139, 1)
  END = (1, 139)

iterator neighbors(a: Vec2): Vec2 = 
  for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
    if a + dir in MAZE: yield a + dir

var
  scores = Table[(Vec2, Vec2), int]()
  best_sets = HashSet[Vec2]()
  heap = HeapQueue[State]()
  new_score, best_score: int
  new_dir: Vec2
  state: State

heap.push (0, START, (0, 1), @[])
while heap.len > 0:
  state = heap.pop
  if state.pos == END:
    best_score = state.score
    for seat in state.seats:
      best_sets.incl seat
    continue
  
  for neighbor in state.pos.neighbors:
    new_dir = neighbor - state.pos
    new_score = state.score + (if new_dir == state.dir: 1 else: 1001)
    if scores.getOrDefault((neighbor, new_dir), new_score) >= new_score:
      scores[(neighbor, new_dir)] = new_score
      heap.push (new_score, neighbor, new_dir, state.seats.concat @[state.pos])

echo "Score: ", best_score
echo "Seats: ", best_sets.len + 1
