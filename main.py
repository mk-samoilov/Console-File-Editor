import curses
import sys

from cfe_core import CFEditor


def display_menu(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    menu_title = "CFEditor Menu"
    menu_items = ["Open file", "Exit"]
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 2, menu_title, curses.A_REVERSE)


        for idx, item in enumerate(menu_items):
            x = 2
            y = 2 + idx
            if idx == current_row:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, item)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, item)

        content = "Welcome in Console File Editor!\n\nTo immediately open file editing you can use the arg <filename>\n(if the file is not found it will be created)\n\nLink on main github repository:\nhttps://github.com/mk-samoilov/Console-File-Editor"

        content_lines = content.split("\n")
        for idx, line in enumerate(content_lines):
            stdscr.addstr(1 + idx, width // 4 + 2, line)

        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                return open_file(stdscr)
            else:
                return None


def open_file(stdscr):
    curses.echo()
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    prompt = "Enter the filename (if the file is not found it will be created):"
    stdscr.addstr(height // 2, (width - len(prompt)) // 2, prompt)
    stdscr.addstr(height // 2 + 1, width // 3, "")
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
