import json


class AppState:
    def __init__(self):
        self._data = {}

    def set_data(self, key, value):
        self._data[key] = value

    def get_data(self, key):
        return self._data.get(key, None)

    def remove_data(self, key):
        if key in self._data:
            del self._data[key]

    def save_state(self, file_name):
        with open(file_name, 'w') as f:
            json.dump(self._data, f)

    def load_state(self, file_name):
        try:
            with open(file_name, 'r') as f:
                self._data = json.load(f)
        except FileNotFoundError:
            pass


appState = AppState()
