"""Simple in-memory state manager for the GUI session."""


class StateManager:
    def __init__(self):
        self._state = {}

    def set(self, key, value):
        self._state[key] = value

    def get(self, key, default=None):
        return self._state.get(key, default)

    def delete(self, key):
        if key in self._state:
            del self._state[key]
