# tactical_grid.py
import random
from utils import get_valid_int, parse_coordinate

class TacticalGrid:
    def __init__(self, target_distance: int):
        self.size = 5
        self.target_distance = target_distance
        # 初始化 5x5 空棋盘
        self.board = [[' ' for _ in range(5)] for _ in range(5)]

    def display(self):
        for row in self.board:
            print("".join(f"[{cell}]" for cell in row))

    def get_empty_cells(self):
        return [(r, c) for r in range(5) for c in range(5) if self.board[r][c] == ' ']

    def is_full(self) -> bool:
        return len(self.get_empty_cells()) == 0

    def apply_rules(self):
        """
        规则扫描：
        若格子中的棋子在水平、垂直或对角线上被对手棋子双向包围（夹攻），则被翻转。
        使用临时棋盘保存更新，避免连锁反应顺序干扰。
        """
        # 四个对称方向：水平、垂直、主对角线、副对角线
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        new_board = [row.copy() for row in self.board]

        for r in range(5):
            for c in range(5):
                curr = self.board[r][c]
                if curr in ['O', 'X']:
                    opp = 'X' if curr == 'O' else 'O'
                    # 检查是否在某个方向被对手夹击
                    for dr, dc in directions:
                        r1, c1 = r - dr, c - dc
                        r2, c2 = r + dr, c + dc
                        if 0 <= r1 < 5 and 0 <= c1 < 5 and 0 <= r2 < 5 and 0 <= c2 < 5:
                            if self.board[r1][c1] == opp and self.board[r2][c2] == opp:
                                new_board[r][c] = opp
                                break  # 只要被一个方向夹击即被同化
        self.board = new_board

    def make_player_move(self, r: int, c: int) -> bool:
        if self.board[r][c] != ' ':
            return False
        self.board[r][c] = 'O'
        self.apply_rules()
        return True

    def make_computer_move(self):
        empty = self.get_empty_cells()
        if empty:
            cr, cc = random.choice(empty)
            self.board[cr][cc] = 'X'
            self.apply_rules()

    def calculate_score(self):
        count_o = sum(row.count('O') for row in self.board)
        count_x = sum(row.count('X') for row in self.board)
        return count_o - count_x

def play_tactical_grid():
    print("Tactical Grid Showdown")
    target = get_valid_int("choose the final distance: ", min_val=1, max_val=25, must_be_odd=True)
    game = TacticalGrid(target)

    while not game.is_full():
        game.display()
        while True:
            # 视频中玩家输入为 0-based 空格分隔，如 '1 1' 或 '0 0'
            r, c = parse_coordinate("your turn: ", max_x=5, max_y=5, zero_indexed=True)
            if game.make_player_move(r, c):
                break
            print("Invalid move! Cell is already occupied.")

        # 玩家走完后，如果棋盘未满，电脑随机走一步
        if not game.is_full():
            game.make_computer_move()

    game.display()
    final_score = game.calculate_score()
    print(f"Final Score (O - X): {final_score}")
    print(f"Target Distance: {game.target_distance}")

    if final_score == game.target_distance:
        print("You Win!")
        return True
    else:
        print("You Lose!")
        return False
