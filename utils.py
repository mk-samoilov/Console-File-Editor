import re
import keyword

SYNTAX_LIGHTING_PATTERNS = [
    ("STRING", r'"(?:\\.|[^"])*"'),
    ("KEYWORD", r"\b(" + "|".join(re.escape(kw) for kw in keyword.kwlist) + r")\b"),
    ("NUMBER", r"\b\d+(\.\d+)?\b")
]

class UndoRedo:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def add_state(self, state):
        self.undo_stack.append(state.copy())
        self.redo_stack.clear()

    def undo(self):
        if len(self.undo_stack) > 1:
            current_state = self.undo_stack.pop()
            self.redo_stack.append(current_state)
            return self.undo_stack[-1]
        return None

    def redo(self):
        if self.redo_stack:
            next_state = self.redo_stack.pop()
            self.undo_stack.append(next_state)
            return next_state
        return None

    def clear(self):
        self.undo_stack.clear()
        self.redo_stack.clear()


def tokenize_line(line):
    tokens = []
    position = 0

    while position < len(line):
        for token_type, pattern in SYNTAX_LIGHTING_PATTERNS:
            match = re.match(pattern, line[position:])
            if match:
                token = match.group(0)
                if token_type == "KEYWORD":
                    if (position == 0 or line[position-1].isspace()) and \
                       (position + len(token) == len(line) or line[position + len(token)].isspace()):
                        tokens.append((token, token_type))
                        position += len(token)
                        break
                else:
                    tokens.append((token, token_type))
                    position += len(token)
                    break
        else:
            tokens.append((line[position], "OTHER"))
            position += 1

    return tokens
