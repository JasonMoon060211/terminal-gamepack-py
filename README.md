Terminal Game Pack: Gameplay and Core Algorithms
This Python-based terminal game collection features three grid-based games: Sliding Puzzle, Bomb Detection Sonar, and Tactical Grid. Each game combines interactive gameplay with fundamental programming concepts, including two-dimensional arrays, randomized state generation, coordinate validation, and rule-based state transitions.

1. Sliding Puzzle — The 8-Puzzle and 15-Puzzle
Overview
Sliding Puzzle is a classic tile-arrangement game played on an extensible N × N grid. Common configurations include the 3 × 3 8-Puzzle and the 4 × 4 15-Puzzle.

The board contains numbered tiles and one empty cell, represented by 0. Players rearrange the tiles by sliding an adjacent tile into the empty cell.

Gameplay
Objective: Restore the tiles to ascending row-major order, starting with 1 in the upper-left corner and ending with the empty cell in the lower-right corner.
Controls: Use W, S, A, and D for directional movement. Each valid move swaps the empty cell with an adjacent tile.
Exit: Enter Q at any time to end the current game and return to the main menu.
For a 3 × 3 board, the target arrangement is:
1 2 3
4 5 6
7 8 0

Core Logic and Algorithms
Solvability and Parity Constraints
A randomly shuffled sliding-puzzle board is not necessarily solvable. For standard N × N boards with N ≥ 2, only half of all possible arrangements are reachable from a fixed solved state through legal moves.

Solvability depends on parity constraints involving the number of inversions. An inversion occurs when a larger numbered tile appears before a smaller one in the flattened board, excluding the empty cell. For even-width boards, the empty cell’s row position must also be taken into account.

Consequently, blindly shuffling the tiles can produce an unsolvable puzzle, making successful completion impossible regardless of the player’s strategy.

Scrambling Through Legal Moves
To avoid unsolvable boards, the engine starts from the solved configuration and performs at least 100 legal random moves of the empty cell.

Because every move is reversible, reversing the scrambling sequence always provides a valid path back to the solved state. This guarantees that every generated board is solvable.

However, the number of scrambling moves does not directly measure puzzle difficulty: random moves may undo earlier moves or revisit previous states. A robust generator should also reject a final board that is already solved.

Coordinate Mapping and Boundary Protection
The board is stored as a two-dimensional array. For an empty cell at (r, c), a proposed move uses a directional offset (dr, dc) to calculate:

next_row = r + dr
next_col = c + dc

The swap is performed only when:

0 <= next_row < N
0 <= next_col < N

Otherwise, the move is rejected and the player receives feedback.

This validation prevents out-of-range access and unintended negative indexing, ensuring that movement cannot wrap around the board’s edges.

2. Bomb Detection Sonar
Overview
Bomb Detection Sonar is a grid-based search game that combines hidden-target discovery with distance-based feedback.

Players scan a 5 × 5 grid to locate concealed targets. A limited energy budget restricts the number of available scans, encouraging players to interpret clues instead of checking every cell indiscriminately.

Gameplay
Objective: Discover all hidden targets before the scanning energy runs out.
Controls: Enter a row and column separated by a space, such as 2 3.
Direct hit: Scanning a target’s location marks that target as found.
Miss: An unsuccessful scan reports the distance to the nearest undiscovered target and the number of threats in the surrounding eight cells.
End conditions: The player wins by finding every target and loses if the scan budget is exhausted while targets remain.
Core Logic and Algorithms
Random Placement Without Overlap
The engine uses Python’s standard-library function random.sample() to select distinct positions from the flattened grid index range:

0 to rows × columns − 1

Each selected index is converted into a two-dimensional coordinate:

row = index // columns
column = index % columns

Because sampling is performed without replacement, no two targets occupy the same cell.

This approach also separates random position selection from coordinate conversion, keeping the placement logic straightforward and reusable.

Distance-Based Search Feedback
The engine evaluates the distance between the scanned cell and undiscovered targets using grid-based distance metrics.

Manhattan distance measures separation along horizontal and vertical directions:

distance = |r1 − r2| + |c1 − c2|

Chebyshev distance measures the minimum number of steps when diagonal movement is also permitted:

distance = max(|r1 − r2|, |c1 − c2|)

For the selected metric, the reported value is the minimum distance to any remaining target.

These clues help players narrow the search area and compare candidate locations. They do not necessarily reveal a unique target position, so successful play requires combining information from multiple scans.

Safe Eight-Neighbor Inspection
To count nearby threats, the engine examines the cells surrounding the scanned position. The search ranges are clipped to the grid boundaries:

for nr in range(max(0, r - 1), min(rows, r + 2)):
    for nc in range(max(0, c - 1), min(columns, c + 2)):
        if (nr, nc) == (r, c):
            continue
            
Excluding the scanned cell leaves at most eight neighbors. Boundary clipping ensures that scans near an edge or corner do not inspect invalid coordinates.

3. Tactical Grid
Overview
Tactical Grid is a turn-based territory-control game in which the player and the computer place distinct markers on a shared board.

Each move changes the available space and influences future opportunities for expansion, blocking, and local competition.

Gameplay
Objective: Gain a positional or territorial advantage under the chosen victory rule.
Controls: Enter a row and column to place a marker in an empty cell.
Turn progression: The player and the computer take turns placing their markers.
Victory conditions: Depending on the intended ruleset, the winner is determined either by comparing controlled-cell totals when the board is full or by being the first to form a required continuous line.
These are alternative victory conditions and should be explicitly defined before play so that players understand what constitutes a win.

Core Logic and Algorithms
A Three-Stage Move Validation Pipeline
Every proposed move must pass three checks:

Input format validation
        ↓
Coordinate range validation
        ↓
Empty-cell validation
        ↓
Move execution

Input format: Confirm that the input can be interpreted as a row and column.
Coordinate range: Check that both coordinates fall within the board.
Cell availability: Verify that the destination cell is empty.
The board is updated only after all three checks succeed. An invalid move should leave the board unchanged and prompt the player to try again.

Protection Against Illegal Overwrites
Attempts to place a marker on an occupied cell are rejected.

This preserves existing placements and prevents invalid input from corrupting the board state. Under placement-only rules, each successful move fills exactly one previously empty cell, so the game progresses toward a full board.

Separating validation from move execution also makes the rules easier to test: malformed input, out-of-range coordinates, and occupied cells can each be checked independently.

Video Instruction
https://github.com/user-attachments/assets/176796a7-58df-4610-9d80-87132fc483c5

