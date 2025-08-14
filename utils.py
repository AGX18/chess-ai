import os
import pygame
from const import *
import chess
def get_clicked_img(piece):
    """Get the clicked piece image"""
    image_dir = os.path.join("images", normal_pieces)
    if not os.path.exists(image_dir):
        raise FileNotFoundError(f"Image directory not found: {image_dir}")
    filename = f"{get_piece_name(piece)}.png"
    path = os.path.join(image_dir, filename)

    try:
        img = pygame.image.load(path)
        return img
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")

def get_piece_name(piece):
    """Get the piece name"""
    color = 'w' if piece.color == chess.WHITE else 'b'
    return color + piece.symbol().upper()