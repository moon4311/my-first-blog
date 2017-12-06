import pyautogui as gui


class Parent(object):
    def __init__(self):
        self.value = 5

    def get_value(self):
        return self.value


class Child(gui):
    def get_value(self):
        return self.value + 1


b = Parent()
c = Child()
print(b.get_value())
print(c.get_value())