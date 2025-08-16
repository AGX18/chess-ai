import pygame
import random
import sys
import ai_player
from const import *
from game import Game
import chess
from random_agent import RandomAgent
from optimized_ai import OptimizedAI
import stalemate

class Main:
    # Fonts

    def __init__(self):
        pygame.init()
        self.SETUP_WIDTH, self.SETUP_HEIGHT = 1400, 800
        self.screen = pygame.display.set_mode((self.SETUP_WIDTH, self.SETUP_HEIGHT))
        self.game = Game()
        # self.non_move = 0
        self.white_player = None
        self.black_player = None
        self.config = self.setup_loop()
        self.set_options()
        pygame.display.set_caption("Chess AI")

    def start_screen(self):
        screen = self.screen
        # Display the start screen elements (title, instructions, etc.)
        font = pygame.font.Font(None, 74)
        text = font.render("Chess AI", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()
        pygame.time.wait(2000)  # Show start screen for 2 seconds

    def set_options(self):
        self.set_white_player()
        self.set_black_player()
        self.set_ai_depth

    def set_white_player(self):
        choice = self.config['white']
        if choice == 'ai':
            self.white_player = ai_player.ChessAI(chess.WHITE, self.game.board)
        elif choice == 'random':
            self.white_player = RandomAgent(chess.WHITE, self.game.board)
        elif choice == 'optimized':
            self.white_player = OptimizedAI(chess.WHITE, self.game.board)
            
    def set_black_player(self):
        choice = self.config['black']
        if choice == 'ai':
            self.black_player = ai_player.ChessAI(chess.BLACK, self.game.board)
        elif choice == 'random':
            self.black_player = RandomAgent(chess.BLACK, self.game.board)
        elif choice == 'optimized':
            self.black_player = OptimizedAI(chess.BLACK, self.game.board)

    
    def set_ai_depth(self):
        self.ai_depth = self.config["ai_depth"] # depth used in ai_player



    def main_loop(self):
        # change the height and width of the screen to the ones used in the chess game
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        while True:
            if game.board.is_checkmate() or game.board.is_game_over() or game.board.can_claim_fifty_moves():
                result = game.board.result()
                print(result)
                print("number of moves:", game.board.fullmove_number)
                winner = "Draw"
                if result == "1-0":
                    winner = "White"
                elif result == "0-1":
                    winner = "Black"
                # winner = "White" if game.board.turn == chess.BLACK else "Black"
                choice = self.show_checkmate_screen(winner)
                if choice == "restart":
                    game.board = chess.Board()  # Reset board
                    self.set_options()
                    continue  # Restart game loop
            elif game.board.is_stalemate() or len(list(game.board.legal_moves)) == 0:
                print("stalemate")
                print("number of moves:", game.board.fullmove_number)
                result = stalemate.show_stalemate_screen(screen, game.board)
                if result == 'restart':
                    board = chess.Board()  # New game
                elif result == 'menu':
                    self.config = self.setup_loop()
                    self.set_options()
                else:
                    pygame.quit()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and ((self.white_player is None and game.board.turn == chess.WHITE) or (self.black_player is None and game.board.turn == chess.BLACK)):
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
                            from_square = dragger.get_origin_square()
                            if from_square:
                                game.board.push(chess.Move(from_square, square))
                    dragger.undrag_piece()

            game.draw_board(screen)
            pygame.display.update()

            
            # if ai player's turn
            if self.white_player and game.board.turn == chess.WHITE:
                move = self.white_player.get_move()
                if move and move in game.board.legal_moves:
                    game.board.push(move)
            elif self.black_player and game.board.turn == chess.BLACK:
                move = self.black_player.get_move()
                if move and move in game.board.legal_moves:
                    game.board.push(move)


    def setup_loop(self):
        # Button dimensions
        button_width, button_height = 200, 50
        WIDTH = self.SETUP_WIDTH
        HEIGHT = self.SETUP_HEIGHT
        gap = 25
        start_button = pygame.Rect(WIDTH // 2 - 100, 580, 200, 60)
        depth_left = pygame.Rect(WIDTH // 2 - 100 - 50, 500, 50, 50)   # '<'
        depth_right = pygame.Rect(WIDTH // 2 + 100, 500, 50, 50)       # '>'
        # Fonts
        title_font = pygame.font.SysFont("Arial", 60, bold=True)
        label_font = pygame.font.SysFont("Arial", 40)
        option_font = pygame.font.SysFont("Arial", 36)
        small_font = pygame.font.SysFont("Arial", 30)
        screen = self.screen
        def draw_setup_screen():
            screen.fill(DARK_GRAY)

            # Title
            title = title_font.render("Chess Setup", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

            # Subtitle
            instr = label_font.render("Choose Player Types", True, GRAY)
            screen.blit(instr, (WIDTH // 2 - instr.get_width() // 2, 130))

            # === White Player ===
            white_label = label_font.render("White:", True, WHITE)
            screen.blit(white_label, (WIDTH // 3 - 250, 220))

            for i in range(len(player_types)):
                color = GREEN if i == white_choice else GRAY
                rect = pygame.Rect((WIDTH // 3 - 60 + i * (button_width + gap), 220, button_width, button_height))
                pygame.draw.rect(screen, color, rect)
                text = option_font.render(player_types[i], True, WHITE)
                screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

            # === Black Player ===
            black_label = label_font.render("Black:", True, WHITE)
            screen.blit(black_label, (WIDTH // 3 - 250, 300))

            for i in range(len(player_types)):
                color = GREEN if i == black_choice else GRAY
                rect = pygame.Rect((WIDTH // 3 - 60 + i * (button_width + gap), 300, button_width, button_height))
                pygame.draw.rect(screen, color, rect)
                text = option_font.render(player_types[i], True, WHITE)
                screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

            # === AI Depth Control ===
            depth_label = label_font.render("AI Search Depth:", True, WHITE)
            screen.blit(depth_label, (WIDTH // 2 - depth_label.get_width() // 2, 400))

            # Depth display
            depth_value = small_font.render(f"{ai_depth}", True, HIGHLIGHT)
            value_rect = pygame.Rect(WIDTH // 2 - 30, 510, 60, 30)
            pygame.draw.rect(screen, BLUE, value_rect, border_radius=8)
            screen.blit(depth_value, (value_rect.centerx - depth_value.get_width() // 2,
                                    value_rect.centery - depth_value.get_height() // 2))

            # Arrows
            left_arrow = small_font.render("<", True, WHITE)
            right_arrow = small_font.render(">", True, WHITE)
            pygame.draw.rect(screen, RED, depth_left, border_radius=10)
            pygame.draw.rect(screen, RED, depth_right, border_radius=10)
            screen.blit(left_arrow, (depth_left.centerx - left_arrow.get_width() // 2,
                                    depth_left.centery - left_arrow.get_height() // 2))
            screen.blit(right_arrow, (depth_right.centerx - right_arrow.get_width() // 2,
                                    depth_right.centery - right_arrow.get_height() // 2))

            # Start Button
            pygame.draw.rect(screen, BLUE, start_button, border_radius=12)
            start_text = label_font.render("Start Game", True, WHITE)
            screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2,
                                    start_button.centery - start_text.get_height() // 2))

            pygame.display.flip()

        # now the function that calls it
        global white_choice, black_choice, ai_depth
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

                    # White options
                    for i in range(len(player_types)):
                        rect = pygame.Rect((WIDTH // 3 - 60 + i * (button_width + gap), 220, button_width, button_height))
                        if rect.collidepoint(mouse_pos):
                            white_choice = i

                    # Black options
                    for i in range(len(player_types)):
                        rect = pygame.Rect((WIDTH // 3 - 60 + i * (button_width + gap), 300, button_width, button_height))
                        if rect.collidepoint(mouse_pos):
                            black_choice = i

                    # Depth controls
                    if depth_left.collidepoint(mouse_pos):
                        ai_depth = max(1, ai_depth - 1)
                    if depth_right.collidepoint(mouse_pos):
                        ai_depth = min(5, ai_depth + 1)

                    # Start Game
                    if start_button.collidepoint(mouse_pos):
                        return {
                            'white': player_types[white_choice].lower(),
                            'black': player_types[black_choice].lower(),
                            'ai_depth': ai_depth
                        }


    def show_checkmate_screen(self, winner):
        screen = self.screen
        """
        Display a checkmate screen with winner and options.
        :param screen: Pygame screen surface
        :param winner: "White" or "Black"
        """

        # Fonts
        font = pygame.font.SysFont("Arial", 70, bold=True)
        small_font = pygame.font.SysFont("Arial", 40)

        # Buttons
        play_again_button = pygame.Rect(250, 400, 300, 60)
        quit_button = pygame.Rect(250, 500, 300, 60)

        clock = pygame.time.Clock()
        while True:
            clock.tick(30)

            # Background
            screen.fill(BLACK)

            # Title
            if winner != "Draw":
                title_text = font.render("Checkmate!", True, RED)
            else:
                title_text = font.render("Tie!", True, RED)

            screen.blit(title_text, (400 - title_text.get_width() // 2, 150))

            # Winner
            if winner != "Draw":
                winner_text = font.render(f"{winner} Wins!", True, WHITE)
            else:
                winner_text = font.render(f"Nobody won!", True, WHITE)

            screen.blit(winner_text, (400 - winner_text.get_width() // 2, 230))

            # Buttons
            pygame.draw.rect(screen, GREEN, play_again_button)
            pygame.draw.rect(screen, GRAY, quit_button)

            play_text = small_font.render("Play Again", True, WHITE)
            quit_text = small_font.render("Quit", True, WHITE)

            screen.blit(play_text, (play_again_button.centerx - play_text.get_width() // 2,
                                    play_again_button.centery - play_text.get_height() // 2))
            screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2,
                                    quit_button.centery - quit_text.get_height() // 2))

            pygame.display.flip()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_button.collidepoint(event.pos):
                        return "restart"  # Signal to restart the game
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()


main = Main()
main.main_loop()
