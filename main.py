import curses
import argparse
from cfe_core import CFEditor

def main(stdscr, filename):
    curses.curs_set(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    editor = CFEditor(stdscr, filename)
    editor.run()

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Console File Editor")
        parser.add_argument("filename", help="File to edit")
        args = parser.parse_args()

        curses.wrapper(main, args.filename)

    except KeyboardInterrupt:
        pass
