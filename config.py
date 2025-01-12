import curses

class CFEConfiguration:
    def __init__(self, core_class_instance):
        self.core = core_class_instance

        self.KEYS_BIND = \
            {
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
