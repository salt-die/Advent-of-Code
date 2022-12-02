include aoc

let CALORIES = fetch(2022, 1).split("\n\n").mapIt(sum it.extract_ints)

part 1: CALORIES.max
part 2: sum CALORIES.nlargest(3)