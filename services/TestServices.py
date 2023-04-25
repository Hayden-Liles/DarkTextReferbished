from AppState import appState

class TestServices:
    def __init__(self):
        pass

    def load(self):
        appState.load_state('save.json')

    def test(self):
        appState.set_data('name', 'aaaaa')
        appState.save_state('save.json')


testServices = TestServices()