import pygame
from const import *
import chess
import os
from dragger import Dragger

class Game:

    def __init__(self):
        self.IMAGES = {}
        self.board = chess.Board()
        self.load_images()
        self.dragger = Dragger()


    def draw_board(self, screen):
        """Draw the chess board and pieces"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, color, rect)

        if self.dragger.is_dragging():
            self.highlight_valid_moves(screen, self.dragger.get_origin_square())
            self.dragger.update_blit(screen)
        self.show_pieces(screen)

    def show_pieces(self, screen):
        """Draw all pieces on the board"""
        for square in chess.SQUARES:
            if self.dragger.is_dragging():
                if square == self.dragger.get_origin_square():
                    continue
            piece = self.board.piece_at(square)
            if piece is not None:
                color = 'w' if piece.color == chess.WHITE else 'b'
                symbol = piece.symbol().lower()
                key = color + symbol.upper()

                if key in self.IMAGES:
                    # Convert square to file (col) and rank (row)
                    col = chess.square_file(square)
                    row = 7 - chess.square_rank(square)  # Flip Y for correct orientation
                    x = col * SQUARE_SIZE  + SQUARE_SIZE // 2
                    y = row * SQUARE_SIZE  + SQUARE_SIZE // 2
                    piece_rect = self.IMAGES[key].get_rect(center=(x, y))
                    screen.blit(self.IMAGES[key], piece_rect)
                else:
                    print(f"❌ No image for {key}")


    def load_images(self):
        """Load all piece images and scale them to SQUARE_SIZE"""
        pieces = ['wK', 'wQ', 'wR', 'wB', 'wN', 'wP',
                  'bK', 'bQ', 'bR', 'bB', 'bN', 'bP']
        
        # Ensure the images directory exists
        image_dir = os.path.join("images", normal_pieces)
        if not os.path.exists(image_dir):
            raise FileNotFoundError(f"Image directory not found: {image_dir}")

        for piece in pieces:
            filename = f"{piece}.png"
            path = os.path.join(image_dir, filename)
            
            if not os.path.exists(path):
                print(f"Warning: Image not found: {path}")
                continue  # Skip missing images

            try:
                img = pygame.image.load(path)
                # Scale image to fit square size
                # img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
                self.IMAGES[piece] = img
            except pygame.error as e:
                print(f"Error loading image {path}: {e}")

    def get_piece_valid_moves(self, square):
        """Get all valid moves for a piece at the given square"""
        if square is None:
            return []
        piece = self.board.piece_at(square)
        if piece is None:
            return []

        # Get all legal moves for the piece
        legal_moves = []
        for move in self.board.legal_moves:
            if move.from_square == square:
                legal_moves.append(move)

        return legal_moves

    def highlight_valid_moves(self, screen, square):
        """Highlight all valid moves for a piece at the given square"""
        valid_moves = self.get_piece_valid_moves(square)
        for move in valid_moves:
            col = chess.square_file(move.to_square)
            row = 7 - chess.square_rank(move.to_square)  # Flip Y for correct orientation
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, highlighted_squares_light if (row + col) % 2 == 0 else highlighted_squares_dark, rect)
