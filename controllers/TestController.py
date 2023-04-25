from services.TestServices import testServices


class TestController:
    def __init__(self):
        pass

    def load(self):
        testServices.load()

    def test(self):
        testServices.test()


testController = TestController()
