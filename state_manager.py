
class StateManager:
    def __init__(self, game):
        self.game = game
        self.state_stack = []

    def push(self, state):
        self.state_stack.append(state)
        state.enter()

    def pop(self):
        if self.state_stack:
            state = self.state_stack.pop()
            state.exit()

    def current(self):
        return self.state_stack[-1] if self.state_stack else None

    def update(self):
        if self.current():
            self.current().update()

    def draw(self, surface):
        if self.current():
            self.current().draw(surface)

class BaseState:
    def __init__(self, manager):
        self.manager = manager

    def enter(self): pass
    def exit(self): pass
    def update(self): pass
    def draw(self, surface): pass
