import curses

class CFEConfiguration:
    def __init__(self, core_class_instance = None):
        self.core = core_class_instance

        self.KEYS_BIND = \
            { # (Backspace binned several times because different OS have different button codes)
                ord("\n"): self.core.insert_newline,                # Enter
                curses.KEY_BACKSPACE: self.core.backspace,          # Backspace
                127: self.core.backspace,                           # Backspace
                8: self.core.backspace,                             # Backspace
                curses.KEY_DC: self.core.delete,                    # Delete
                curses.KEY_LEFT: self.core.move_cursor_left,        # Move Left
                curses.KEY_RIGHT: self.core.move_cursor_right,      # Move Right
                curses.KEY_UP: self.core.move_cursor_up,            # Move Up
                curses.KEY_DOWN: self.core.move_cursor_down         # Move Down
            }

        self.COLOR_PAIRS = \
            [
                {"pair-code": 1, "text": curses.COLOR_BLUE, "background": curses.COLOR_BLACK},
                {"pair-code": 2, "text": curses.COLOR_GREEN, "background": curses.COLOR_BLACK},
                {"pair-code": 3, "text": curses.COLOR_YELLOW, "background": curses.COLOR_BLACK},
                {"pair-code": 4, "text": curses.COLOR_CYAN, "background": curses.COLOR_BLACK}
            ]

        self.SYNTAX_LIGHTING_COLORS = \
            { # (By pair-code)
                "KEYWORD": 3,
                "STRING": 2,
                "NUMBER": 4
            }
