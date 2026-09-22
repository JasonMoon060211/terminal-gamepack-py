# bomb_detection.py
import random
from utils import get_valid_int, parse_coordinate

class BombDetection:
    def __init__(self, size: int, bomb_count: int):
        self.size = size
        self.bomb_count = bomb_count
        # 生成不重复的炸弹绝对坐标 (r, c)
        all_cells = [(r, c) for r in range(size) for c in range(size)]
        self.bombs = set(random.sample(all_cells, bomb_count))
        self.found_bombs = set()
        # 棋盘状态矩阵：'X' 未勘探, 'O' 找到的炸弹, '#' 已勘探无炸弹
        self.board = [['X' for _ in range(size)] for _ in range(size)]
        self.steps = 1

    def display(self):
        for row in self.board:
            print("".join(row))

    def probe(self, r: int, c: int):
        """勘探指定坐标"""
        if (r, c) in self.bombs:
            if (r, c) not in self.found_bombs:
                self.found_bombs.add((r, c))
                self.board[r][c] = 'O'
                print(f"you find bomb {len(self.found_bombs)}")
        else:
            self.board[r][c] = '#'
            # 计算同列与同行的剩余炸弹曼哈顿距离
            active_bombs = self.bombs - self.found_bombs
            col_dist = sum(abs(br - r) for br, bc in active_bombs if bc == c)
            row_dist = sum(abs(bc - c) for br, bc in active_bombs if br == r)
            print(f"({col_dist}, {row_dist})")

    def all_bombs_found(self) -> bool:
        return len(self.found_bombs) == self.bomb_count

def play_bomb_detection():
    print("Bombs Detection")
    size = get_valid_int("side length: ", min_val=2, max_val=20)
    # 炸弹数量约束：必须小于边长的两倍
    max_bombs = 2 * size - 1
    bomb_count = get_valid_int(f"bombs number (less than {2 * size}): ", min_val=1, max_val=max_bombs)

    game = BombDetection(size, bomb_count)

    while not game.all_bombs_found():
        print(f"step {game.steps}")
        game.display()
        r, c = parse_coordinate("choose a position: ", max_x=size, max_y=size, zero_indexed=False)
        game.probe(r, c)
        game.steps += 1

    game.display()
    print("You win!")
