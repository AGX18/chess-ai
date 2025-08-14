class Dragger:

    def __init__(self):
        self.mouseX = 0
        self.mouseY = 0

    def update_mouse_position(self, pos):
        self.mouseX, self.mouseY = pos