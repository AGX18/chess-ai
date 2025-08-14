import pygame
import random
import sys
import ai_player
from const import *
from game import Game
import chess

class Main:
    # Fonts

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()

        pygame.display.set_caption("Chess AI")

    def start_screen(self):
        screen = self.screen
        # Display the start screen elements (title, instructions, etc.)
        font = pygame.font.Font(None, 74)
        text = font.render("Chess AI", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()
        pygame.time.wait(2000)  # Show start screen for 2 seconds

    def main_loop(self):
        config = self.setup_loop()
        white_player = ai_player.ChessAI(chess.WHITE, self.game.board) if config['white'] == 'ai' else None
        black_player = ai_player.ChessAI(chess.BLACK, self.game.board) if config['black'] == 'ai' else None
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and ((white_player is None and game.board.turn == chess.WHITE) or (black_player is None and game.board.turn == chess.BLACK)):
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
                    if dragger.is_dragging():
                        row = 7 - (dragger.mouseY // SQUARE_SIZE)
                        col = dragger.mouseX // SQUARE_SIZE
                        square = chess.square(col, row)
                        valid_moves = game.get_piece_valid_moves(dragger.get_origin_square())
                        if square in [m.to_square for m in valid_moves]:
                            game.board.push(chess.Move(dragger.get_origin_square(), square))
                    dragger.undrag_piece()

            game.draw_board(screen)
            pygame.display.update()

            # if ai player's turn
            if white_player and game.board.turn == chess.WHITE:
                move = white_player.get_move()
                if move:
                    game.board.push(move)
            elif black_player and game.board.turn == chess.BLACK:
                move = black_player.get_move()
                if move:
                    game.board.push(move)


    def setup_loop(self):
        title_font = pygame.font.SysFont("Arial", 60, bold=True)
        label_font = pygame.font.SysFont("Arial", 40)
        option_font = pygame.font.SysFont("Arial", 36)
        start_button = pygame.Rect(WIDTH // 2 - 100, 450, 200, 60)
        screen = self.screen
        def draw_setup_screen():
            screen.fill((30, 30, 40))  # Dark background
            

            # Title
            title = title_font.render("Chess Setup", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

            # Instructions
            instr = label_font.render("Choose Player Types", True, GRAY)
            screen.blit(instr, (WIDTH // 2 - instr.get_width() // 2, 130))

            # White player
            white_label = label_font.render("White:", True, WHITE)
            screen.blit(white_label, (WIDTH // 2 - 200, 220))

            # White buttons
            for i, option in enumerate(player_options):
                color = GREEN if i == white_choice else GRAY
                rect = pygame.Rect((WIDTH // 2 - 60 + i * (button_width + gap), 220, button_width, button_height))
                pygame.draw.rect(screen, color, rect)
                text = option_font.render(option, True, WHITE)
                screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

            # Black player
            black_label = label_font.render("Black:", True, WHITE)
            screen.blit(black_label, (WIDTH // 2 - 200, 300))

            # Black buttons
            for i, option in enumerate(player_options):
                color = GREEN if i == black_choice else GRAY
                rect = pygame.Rect((WIDTH // 2 - 60 + i * (button_width + gap), 300, button_width, button_height))
                pygame.draw.rect(screen, color, rect)
                text = option_font.render(option, True, WHITE)
                screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

            # Start Game Button
            pygame.draw.rect(screen, BLUE, start_button)
            start_text = label_font.render("Start Game", True, WHITE)
            screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2,
                                    start_button.centery - start_text.get_height() // 2))

            pygame.display.flip()
        global white_choice, black_choice
        clock = pygame.time.Clock()

        while True:
            clock.tick(30)
            draw_setup_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    # Check White options
                    for i in range(2):
                        rect = pygame.Rect((WIDTH // 2 - 60 + i * (button_width + gap), 220, button_width, button_height))
                        if rect.collidepoint(mouse_pos):
                            white_choice = i

                    # Check Black options
                    for i in range(2):
                        rect = pygame.Rect((WIDTH // 2 - 60 + i * (button_width + gap), 300, button_width, button_height))
                        if rect.collidepoint(mouse_pos):
                            black_choice = i

                    # Check Start button
                    if start_button.collidepoint(mouse_pos):
                        # Return the choices: e.g., {'white': 'human', 'black': 'ai'}
                        return {
                            'white': 'human' if white_choice == 0 else 'ai',
                            'black': 'human' if black_choice == 0 else 'ai'
                        }



main = Main()
main.main_loop()
