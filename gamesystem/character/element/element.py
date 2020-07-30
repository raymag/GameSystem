import random 

class Element:
    def __init__(self, name, modifiers = (0, 0, 0, 0, 0, 0)):
        self.__name = name
        self.__modifiers = modifiers

    def get_name(self):
        return self.__name

    def get_modifiers(self):
        return self.__modifiers

class Air(Element):
    def __init__(self):
        super().__init__('air', (0, 1, -1, 0, 0, 0))

class Earth(Element):
    def __init__(self):
        super().__init__('earth', (0, -1, 1, 0, 0, 0))

class Fire(Element):
    def __init__(self):
        super().__init__('fire', (1, 0, 0, -1, 0, 0))

class Water(Element):
    def __init__(self):
        super().__init__('water', (-1, 0, 0, 1, 0, 0))

def random_element():
    return random.choice([Air(), Earth(), Fire(), Water()])