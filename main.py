import pygame
import random
import sys
import ai_player
from const import *
from game import Game
import chess

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()

        pygame.display.set_caption("Chess AI")

    def main_loop(self):
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse_position(event.pos)
                    row = 7 - (dragger.mouseY // SQUARE_SIZE)  # flipped y
                    col = dragger.mouseX // SQUARE_SIZE
                    square = chess.square(col, row)
                    piece = game.board.piece_at(square)
                    if piece:  # assuming player is White
                        color = 'w' if piece.color == chess.WHITE else 'b'
                        x, y = event.pos
                        col = x // SQUARE_SIZE
                        row = 7 - (y // SQUARE_SIZE)  # Flip Y to match chess board
                        dragger.save_origin_square(chess.square(col, row))
                        dragger.drag_piece(piece)
                        # Store selected square and highlight it
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.is_dragging():
                        dragger.update_mouse_position(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece()

            game.draw_board(screen)
            if dragger.is_dragging():
                dragger.update_blit(screen)
            pygame.display.update()
            



main = Main()
main.main_loop()
