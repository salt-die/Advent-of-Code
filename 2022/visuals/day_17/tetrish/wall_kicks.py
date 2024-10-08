J_WALL_KICKS = {
    # Clockwise rotations
    (0, 1): (( 0,  0), ( 0, -1), (-2, -1), ( 2,  0), ( 2, -1)),
    (1, 2): (( 0,  0), ( 0,  1), ( 2,  1), (-2,  0), (-2,  1)),
    (2, 3): (( 0,  0), ( 0,  1), (-2,  1), ( 2,  0), ( 2,  1)),
    (3, 0): (( 0,  0), ( 0, -1), ( 2, -1), (-2,  0), (-2, -1)),

    # Counter-clockwise rotations
    (1, 0): (( 0,  0), ( 0,  1), ( 2,  1), (-2,  0), (-2,  1)),
    (2, 1): (( 0,  0), ( 0, -1), (-2, -1), ( 2,  0), ( 2, -1)),
    (3, 2): (( 0,  0), ( 0, -1), ( 2, -1), (-2,  0), (-2, -1)),
    (0, 3): (( 0,  0), ( 0,  1), (-2,  1), ( 2,  0), ( 2,  1)),
}

I_WALL_KICKS = {
    # Clockwise rotations
    (0, 1): (( 0,  0), ( 0, -2), ( 0,  1), ( 1, -2), (-2,  1)),
    (1, 2): (( 0,  0), ( 0, -1), ( 0,  2), (-2, -1), ( 1,  2)),
    (2, 3): (( 0,  0), ( 0,  2), ( 0, -1), (-1,  2), ( 2, -1)),
    (3, 0): (( 0,  0), ( 0,  1), ( 0, -2), ( 2,  1), (-1, -2)),

    # Counter-clockwise rotations
    (1, 0): (( 0,  0), ( 0,  2), ( 0, -1), (-1,  2), ( 2, -1)),
    (2, 1): (( 0,  0), ( 0,  1), ( 0, -2), ( 2,  1), (-1, -2)),
    (3, 2): (( 0,  0), ( 0, -2), ( 0,  1), ( 1, -2), (-2,  1)),
    (0, 3): (( 0,  0), ( 0, -1), ( 0,  2), (-2, -1), ( 1,  2)),
}

O_WALL_KICKS = {
    (0, 1): (( 0,  0), ),
    (1, 2): (( 0,  0), ),
    (2, 3): (( 0,  0), ),
    (3, 0): (( 0,  0), ),

    (1, 0): (( 0,  0), ),
    (2, 1): (( 0,  0), ),
    (3, 2): (( 0,  0), ),
    (0, 3): (( 0,  0), ),
}
