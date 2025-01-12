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
