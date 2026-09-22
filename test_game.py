"""
Unit tests for Terminal Game Suite.
Covers core mathematical invariants, boundary protections, and state transitions.
"""

import unittest
import random

class SlidingPuzzleLogic:
    def __init__(self, size=3):
        self.size = size
        self.solved_state = list(range(1, size * size)) + [0]
        self.board = self.solved_state[:]
        self.empty_pos = size * size - 1

    def is_solved(self):
        return self.board == self.solved_state

    def try_move(self, direction):
        """
        direction: 'W' (上), 'S' (下), 'A' (左), 'D' (右)
        """
        r, c = self.empty_pos // self.size, self.empty_pos % self.size
        moves = {
            'W': (-1, 0),
            'S': (1, 0),
            'A': (0, -1),
            'D': (0, 1)
        }
        if direction not in moves:
            return False

        dr, dc = moves[direction]
        nr, nc = r + dr, c + dc

        (0 <= nr < N 且 0 <= nc < N)
        if 0 <= nr < self.size and 0 <= nc < self.size:
            target_idx = nr * self.size + nc
            # 交换空位与目标块
            self.board[self.empty_pos], self.board[target_idx] = self.board[target_idx], self.board[self.empty_pos]
            self.empty_pos = target_idx
            return True
        return False



class BombDetectionLogic:
    @staticmethod
    def generate_bombs(rows, cols, count):
        """利用 random.sample 保证一维索引抽样不重复，再映射为二维"""
        indices = random.sample(range(rows * cols), count)
        return [(idx // cols, idx % cols) for idx in indices]

    @staticmethod
    def manhattan_distance(p1, p2):
        """曼哈顿距离: |r1 - r2| + |c1 - c2|"""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    @staticmethod
    def chebyshev_distance(p1, p2):
        """切比雪夫距离: max(|r1 - r2|, |c1 - c2|)"""
        return max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))

    @staticmethod
    def count_neighbors(r, c, rows, cols, bombs):
        
        count = 0
        for nr in range(max(0, r - 1), min(rows, r + 2)):
            for nc in range(max(0, c - 1), min(cols, c + 2)):
                if (nr, nc) == (r, c):
                    continue
                if (nr, nc) in bombs:
                    count += 1
        return count


class TacticalGridLogic:
    def __init__(self, size=3):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]

    def validate_and_place(self, raw_input, marker):

        try:
            parts = raw_input.strip().split()
            if len(parts) != 2:
                return False, "Input must be two numbers"
            r, c = int(parts[0]), int(parts[1])
        except ValueError:
            return False, "Invalid number format"


        if not (0 <= r < self.size and 0 <= c < self.size):
            return False, "Coordinates out of bounds"


        if self.grid[r][c] != ' ':
            return False, "Cell is already occupied"


        self.grid[r][c] = marker
        return True, "Success"

class TestTerminalGames(unittest.TestCase):


    def test_puzzle_initial_win_condition(self):

        puzzle = SlidingPuzzleLogic(size=3)
        self.assertTrue(puzzle.is_solved(), "Initial state should be solved")

    def test_puzzle_boundary_protection(self):

        puzzle = SlidingPuzzleLogic(size=3)

        self.assertFalse(puzzle.try_move('S'), "Moving DOWN from bottom row must fail")
        self.assertFalse(puzzle.try_move('D'), "Moving RIGHT from rightmost col must fail")
        self.assertEqual(puzzle.empty_pos, 8, "Position should remain unchanged after illegal move")

    def test_puzzle_valid_move(self):

        puzzle = SlidingPuzzleLogic(size=3)

        self.assertTrue(puzzle.try_move('A'))
        self.assertEqual(puzzle.empty_pos, 7)
        self.assertFalse(puzzle.is_solved(), "Board should no longer be solved after move")


        self.assertTrue(puzzle.try_move('D'))
        self.assertTrue(puzzle.is_solved(), "Reversing the move must restore solved state")


    def test_sonar_bomb_generation_uniqueness(self):
        rows, cols, count = 5, 5, 6
        bombs = BombDetectionLogic.generate_bombs(rows, cols, count)
        self.assertEqual(len(bombs), count)
        self.assertEqual(len(set(bombs)), count, "Generated bombs must not contain duplicates")
        for r, c in bombs:
            self.assertTrue(0 <= r < rows and 0 <= c < cols, "Bomb coordinates must be in bounds")

    def test_sonar_distance_metrics(self):
        p1 = (1, 1)
        p2 = (4, 5)
        # 曼哈顿: |1-4| + |1-5| = 3 + 4 = 7
        self.assertEqual(BombDetectionLogic.manhattan_distance(p1, p2), 7)
        # 切比雪夫: max(|1-4|, |1-5|) = max(3, 4) = 4
        self.assertEqual(BombDetectionLogic.chebyshev_distance(p1, p2), 4)

    def test_sonar_neighbor_clipping_at_corner(self):
        rows, cols = 5, 5
        bombs = [(0, 1), (1, 1), (4, 4)]
        count = BombDetectionLogic.count_neighbors(0, 0, rows, cols, bombs)
        self.assertEqual(count, 2)

    def test_tactical_validation_pipeline(self):
        grid_game = TacticalGridLogic(size=3)

        ok, msg = grid_game.validate_and_place("invalid_input", 'X')
        self.assertFalse(ok)

        ok, msg = grid_game.validate_and_place("3 1", 'X')
        self.assertFalse(ok)
        self.assertIn("bounds", msg)

        ok, msg = grid_game.validate_and_place("1 1", 'X')
        self.assertTrue(ok)

        ok, msg = grid_game.validate_and_place("1 1", 'O')
        self.assertFalse(ok)
        self.assertIn("occupied", msg)
        self.assertEqual(grid_game.grid[1][1], 'X', "Occupied cell must not be overwritten")


if __name__ == '__main__':
    unittest.main()
