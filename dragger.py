from const import *
from utils import *
class Dragger:

    def __init__(self):
        self.origin_square = None
        self.dragging = False
        self.piece = None
        self.mouseX = 0
        self.mouseY = 0

    def update_mouse_position(self, pos):
        self.mouseX, self.mouseY = pos

    def save_origin_square(self, square):
        self.origin_square = square

    def drag_piece(self, piece):
        self.dragging = True
        self.piece = piece

    def get_origin_square(self):
        return self.origin_square

    def is_dragging(self):
        return self.dragging

    def get_dragged_piece(self):
        return self.piece

    def undrag_piece(self):
        self.dragging = False
        self.piece = None
        self.origin_square = None

    def update_blit(self, screen):
        img = get_clicked_img(self.piece)
        img_rect = img.get_rect(center=(self.mouseX, self.mouseY))
        # Draw the dragged piece at the mouse position
        screen.blit(img, img_rect)