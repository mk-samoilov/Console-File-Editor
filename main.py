import curses
import sys

from cfe_core import CFEditor


def display_menu(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    menu_title = "  CFEditor Menu"
    menu_items = ["Create a new file", "Exit"]
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, menu_title, curses.A_BOLD)


        for idx, item in enumerate(menu_items):
            x = 2
            y = 2 + idx
            if idx == current_row:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, item)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, item)

        content = "Welcome in Console File Editor!\nTo immediately open file editing you can use the arg <filename>\n\nLink on main github repository:\nhttps://github.com/mk-samoilov/Console-File-Editor"

        content_lines = content.split("\n")
        for idx, line in enumerate(content_lines):
            stdscr.addstr(2 + idx, width // 4 + 2, line)

        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                return create_new_file(stdscr)
            else:
                return None


def create_new_file(stdscr):
    curses.echo()
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    prompt = "Enter the name of the new file: "
    stdscr.addstr(height // 2, (width - len(prompt)) // 2, prompt)
    filename = stdscr.getstr().decode("utf-8")
    curses.noecho()
    return filename


def main(stdscr, filename=None):
    if filename is None:
        filename = display_menu(stdscr)
        if filename is None:
            return

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
        if len(sys.argv) > 1:
            _filename_arg = sys.argv[1]
            curses.wrapper(main, _filename_arg)
        else:
            curses.wrapper(main)
    except KeyboardInterrupt:
        pass
