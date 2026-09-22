# main.py
from ascii_art import BANNER_TITLE, NEXT_LEVEL, THE_END, print_banner
from sliding_puzzle import play_sliding_puzzle
from bomb_detection import play_bomb_detection
from tactical_grid import play_tactical_grid

def main():

    print_banner(BANNER_TITLE)


    play_sliding_puzzle()
    print_banner(NEXT_LEVEL)


    play_bomb_detection()
    print_banner(NEXT_LEVEL)


    play_tactical_grid()


    print_banner(THE_END)

if __name__ == "__main__":
    main()
