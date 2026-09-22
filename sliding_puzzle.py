# sliding_puzzle.py
import random
from utils import get_valid_int

class SlidingPuzzle:
    def __init__(self, size: int):
        self.size = size
        self.board = self._generate_solvable_board()

    def _count_inversions(self, flat_list):
        """计算列表中除去 0 之外的所有逆序对数量"""
        nums = [x for x in flat_list if x != 0]
        swaps = 0
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] > nums[j]:
                    swaps += 1
        return swaps

    def _is_solvable(self, flat_list):
        """
        数学可解性校验：
        - 奇数阶（如 3x3）：逆序数为偶数时有解
        - 偶数阶（如 4x4）：(逆序数 + 空白所在行自底向上行数) 为奇数时有解
        """
        swaps = self._count_inversions(flat_list)
        if self.size % 2 == 1:
            return swaps % 2 == 0
        else:
            blank_idx = flat_list.index(0)
            blank_row_from_bottom = self.size - (blank_idx // self.size)
            return (swaps + blank_row_from_bottom) % 2 == 1

    def _generate_solvable_board(self):
        """循环洗牌直到生成非还原态且必然有解的棋盘"""
        target = list(range(1, self.size * self.size)) + [0]
        flat = target.copy()
        while True:
            random.shuffle(flat)
            if self._is_solvable(flat) and flat != target:
                break
        return [flat[i * self.size:(i + 1) * self.size] for i in range(self.size)]

    def display(self):
        """在终端打印棋盘矩阵"""
        for row in self.board:
            print(" ".join(f"{val:2d}" for val in row))

    def find_blank(self):
        """获取空白块 (0) 的坐标"""
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return r, c
        return -1, -1

    def move(self, direction: str) -> bool:
        """
        视频操作定义：
        w: 空白上方的方块移入空白（空白上移）
        s: 空白下方的方块移入空白（空白下移）
        a: 空白右方的方块移入空白（空白右移）
        d: 空白左方的方块移入空白（空白左移）
        """
        br, bc = self.find_blank()
        target_r, target_c = br, bc

        if direction == 'w':
            target_r = br - 1
        elif direction == 's':
            target_r = br + 1
        elif direction == 'a':
            target_c = bc + 1
        elif direction == 'd':
            target_c = bc - 1
        else:
            return False

        # 边界检查
        if 0 <= target_r < self.size and 0 <= target_c < self.size:
            self.board[br][bc], self.board[target_r][target_c] = self.board[target_r][target_c], self.board[br][bc]
            return True
        return False

    def is_solved(self) -> bool:
        """检验是否按序拼好：1, 2, ..., N^2-1, 0"""
        flat = [val for row in self.board for val in row]
        return flat == list(range(1, self.size * self.size)) + [0]

def play_sliding_puzzle():
    print("Sliding Puzzle")
    size = get_valid_int("Choose game level(3 or 4): ", min_val=3, max_val=4)
    game = SlidingPuzzle(size)

    while not game.is_solved():
        game.display()
        action = input("Enter your move(w/s/a/d): ").strip().lower()
        if action not in ['w', 's', 'a', 'd']:
            print("Invalid input! Please enter 'w', 's', 'a', or 'd'.")
            continue
        moved = game.move(action)
        if not moved:
            print("Invalid move! Can't slide in that direction.")

    game.display()
    print("You win!")
