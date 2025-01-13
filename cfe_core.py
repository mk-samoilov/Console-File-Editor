from config import CFEConfiguration
from utils import UndoRedo

import curses
import os
import keyword
import re

class CFEditor:
    def __init__(self, stdscr, filename: str):
        self.stdscr = stdscr
        self.filename = filename
        self.content = []

        self.cursor_y = 0
        self.cursor_x = 0
        self.top_line = 0
        self.left_margin = 0

        self.search_query = ""
        self.search_results = []
        self.current_result = -1

        self.show_line_numbers = True

        self.undo_redo = UndoRedo()
        self.config = CFEConfiguration(core_class_instance=self)

    def load_file(self):
        if os.path.exists(self.filename):
            with open(file=self.filename, mode="r", encoding="UTF-8") as file:
                self.content = file.read().splitlines()
        else:
            self.content = [""]
        self.undo_redo.clear()
        self.undo_redo.add_state(self.content)

    def save_file(self):
        with open(file=self.filename, mode="w", encoding="UTF-8") as file:
            file.write("\n".join(self.content))

    def adjust_view(self):
        height, width = self.stdscr.getmaxyx()
        if self.cursor_y < self.top_line:
            self.top_line = self.cursor_y
        elif self.cursor_y >= self.top_line + height - 2:
            self.top_line = self.cursor_y - height + 3

        effective_width = width - (8 if self.show_line_numbers else 0)
        if self.cursor_x < self.left_margin:
            self.left_margin = max(0, self.cursor_x - 5)
        elif self.cursor_x >= self.left_margin + effective_width:
            self.left_margin = self.cursor_x - effective_width + 5

    def display(self):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        for i, line in enumerate(self.content[self.top_line:self.top_line+height-1]):
            if i == height - 1:
                break
            if self.show_line_numbers:
                line_num = str(self.top_line + i + 1).rjust(4)
                self.stdscr.addstr(i, 0, line_num, curses.color_pair(1))
                self.stdscr.addstr(i, 5, "│ ")
                visible_line = line[self.left_margin:self.left_margin+width-8]
                self.stdscr.addstr(i, 7, visible_line)
            else:
                visible_line = line[self.left_margin:self.left_margin+width]
                self.stdscr.addstr(i, 0, visible_line)

        status = f"CFE | File: {self.filename} | Pos: {self.cursor_y+1}:{self.cursor_x+1} | ^S: save | ^F: find | ^L: line numbers | ^Z: undo | ^Y: redo | ^Q: quit"
        self.stdscr.addstr(height-1, 0, status[:width-1], curses.A_REVERSE)

        cursor_y = self.cursor_y - self.top_line
        cursor_x = self.cursor_x - self.left_margin + (7 if self.show_line_numbers else 0)
        self.stdscr.move(cursor_y, cursor_x)
        self.stdscr.refresh()

    @staticmethod
    def syntax_highlight(line):
        keywords = set(keyword.kwlist)
        tokens = re.findall(r"\b\w+\b|[^\w\s]", line)
        highlighted = ""
        for token in tokens:
            if token in keywords:
                highlighted += f"\033[1;35m{token}\033[0m"
            elif token.isdigit():
                highlighted += f"\033[1;36m{token}\033[0m"
            elif token in "()[]{}":
                highlighted += f"\033[1;33m{token}\033[0m"
            else:
                highlighted += token
        return highlighted

    def auto_complete(self):
        current_word = re.findall(r'\w+$', self.content[self.cursor_y][:self.cursor_x])
        if current_word:
            current_word = current_word[0]
            suggestions = [kw for kw in keyword.kwlist if kw.startswith(current_word)]
            if suggestions:
                completion = suggestions[0][len(current_word):]
                self.insert_char(completion)

    def handle_input(self, key):
        if 32 <= key <= 128:
            self.insert_char(chr(key))
        else:
            try:
                self.config.KEYS_BIND[key]()
            except KeyError:
                pass

        self.adjust_view()

    def insert_newline(self):
        self.content.insert(self.cursor_y + 1, self.content[self.cursor_y][self.cursor_x:])
        self.content[self.cursor_y] = self.content[self.cursor_y][:self.cursor_x]
        self.cursor_y += 1
        self.cursor_x = 0
        self.undo_redo.add_state(self.content)

    def backspace(self):
        if self.cursor_x > 0:
            self.content[self.cursor_y] = self.content[self.cursor_y][:self.cursor_x-1] + self.content[self.cursor_y][self.cursor_x:]
            self.cursor_x -= 1
        elif self.cursor_y > 0:
            self.cursor_x = len(self.content[self.cursor_y-1])
            self.content[self.cursor_y-1] += self.content[self.cursor_y]
            self.content.pop(self.cursor_y)
            self.cursor_y -= 1
        self.undo_redo.add_state(self.content)

    def delete(self):
        if self.cursor_x < len(self.content[self.cursor_y]):
            self.content[self.cursor_y] = self.content[self.cursor_y][:self.cursor_x] + self.content[self.cursor_y][self.cursor_x+1:]
        elif self.cursor_y < len(self.content) - 1:
            self.content[self.cursor_y] += self.content[self.cursor_y+1]
            self.content.pop(self.cursor_y+1)
        self.undo_redo.add_state(self.content)

    def move_cursor_right(self):
        if self.cursor_x < len(self.content[self.cursor_y]):
            self.cursor_x += 1
        elif self.cursor_y < len(self.content) - 1:
            self.cursor_y += 1
            self.cursor_x = 0
        self.adjust_view()

    def move_cursor_left(self):
        if self.cursor_x > 0:
            self.cursor_x -= 1
        elif self.cursor_y > 0:
            self.cursor_y -= 1
            self.cursor_x = len(self.content[self.cursor_y])
        self.adjust_view()

    def move_cursor_up(self):
        if self.cursor_y > 0:
            self.cursor_y -= 1
            self.cursor_x = min(self.cursor_x, len(self.content[self.cursor_y]))

    def move_cursor_down(self):
        if self.cursor_y < len(self.content) - 1:
            self.cursor_y += 1
            self.cursor_x = min(self.cursor_x, len(self.content[self.cursor_y]))

    def insert_char(self, char):
        self.content[self.cursor_y] = self.content[self.cursor_y][:self.cursor_x] + char + self.content[self.cursor_y][self.cursor_x:]
        self.cursor_x += 1
        self.undo_redo.add_state(self.content)

    def search(self):
        height, width = self.stdscr.getmaxyx()
        self.stdscr.addstr(height-1, 0, "Search: " + " " * (width-8))
        self.stdscr.move(height-1, 8)
        curses.echo()
        self.search_query = self.stdscr.getstr(height-1, 8, width-9).decode("utf-8")
        curses.noecho()

        self.search_results = []
        for i, line in enumerate(self.content):
            start = 0
            while True:
                index = line.find(self.search_query, start)
                if index == -1:
                    break
                self.search_results.append((i, index))
                start = index + 1

        if self.search_results:
            self.current_result = 0
            self.cursor_y, self.cursor_x = self.search_results[0]

    def next_search_result(self):
        if self.search_results:
            self.current_result = (self.current_result + 1) % len(self.search_results)
            self.cursor_y, self.cursor_x = self.search_results[self.current_result]

    def toggle_line_numbers(self):
        self.show_line_numbers = not self.show_line_numbers

    def undo(self):
        previous_state = self.undo_redo.undo()
        if previous_state:
            self.content = previous_state

    def redo(self):
        next_state = self.undo_redo.redo()
        if next_state:
            self.content = next_state

    def run(self):
        self.load_file()
        while True:
            self.display()
            key = self.stdscr.getch()
            if key == 19:
                self.save_file()
            elif key == 17:
                break
            elif key == 6:
                self.search()
            elif key == 9:
                self.auto_complete()
            elif key == 14:
                self.next_search_result()
            elif key == 12:
                self.toggle_line_numbers()
            elif key == 26:
                self.undo()
            elif key == 25:
                self.redo()
            else:
                self.handle_input(key)
