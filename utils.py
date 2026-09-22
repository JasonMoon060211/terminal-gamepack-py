# utils.py
import re

def get_valid_int(prompt: str, min_val: int = None, max_val: int = None, must_be_odd: bool = False) -> int:

    while True:
        raw = input(prompt).strip()
        if not raw.lstrip('-').isdigit():
            print("Invalid input! Please enter a valid integer.")
            continue
        
        val = int(raw)
        if min_val is not None and val < min_val:
            print(f"Invalid input! Value must be >= {min_val}.")
            continue
        if max_val is not None and val > max_val:
            print(f"Invalid input! Value must be <= {max_val}.")
            continue
        if must_be_odd and (val % 2 == 0):
            print("Invalid input! You must enter an ODD number.")
            continue
            
        return val

def parse_coordinate(prompt: str, max_x: int, max_y: int, zero_indexed: bool = False):

    while True:
        raw = input(prompt).strip()

        nums = re.findall(r'\d+', raw)
        if len(nums) != 2:
            print("Invalid input! Format must be (x, y) or 'x y'.")
            continue
        
        c1, c2 = int(nums[0]), int(nums[1])
        
        if zero_indexed:

            if 0 <= c1 < max_x and 0 <= c2 < max_y:
                return c1, c2
        else:

            if 1 <= c1 <= max_x and 1 <= c2 <= max_y:
                return c1 - 1, c2 - 1
                
        print(f"Invalid position! Coordinate out of boundary.")
