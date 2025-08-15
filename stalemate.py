import pygame
import chess

class StalemateScreen:
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Colors
        self.bg_color = (40, 40, 40)
        self.overlay_color = (0, 0, 0, 180)  # Semi-transparent black
        self.white = (255, 255, 255)
        self.gray = (128, 128, 128)
        self.gold = (255, 215, 0)
        self.button_color = (70, 70, 70)
        self.button_hover = (100, 100, 100)
        self.button_text = (255, 255, 255)
        
        # Fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 64)
        self.subtitle_font = pygame.font.Font(None, 36)
        self.text_font = pygame.font.Font(None, 28)
        self.button_font = pygame.font.Font(None, 32)
        
        # Button properties
        self.button_width = 200
        self.button_height = 50
        self.button_spacing = 20
        
        # Create buttons
        self.create_buttons()
        
        # Animation
        self.animation_offset = 0
        self.animation_speed = 2
        
    def create_buttons(self):
        """Create buttons for the stalemate screen"""
        center_x = self.width // 2
        center_y = self.height // 2 + 100
        
        self.buttons = {
            'new_game': pygame.Rect(
                center_x - self.button_width // 2,
                center_y,
                self.button_width,
                self.button_height
            ),
            'main_menu': pygame.Rect(
                center_x - self.button_width // 2,
                center_y + self.button_height + self.button_spacing,
                self.button_width,
                self.button_height
            ),
            'quit': pygame.Rect(
                center_x - self.button_width // 2,
                center_y + 2 * (self.button_height + self.button_spacing),
                self.button_width,
                self.button_height
            )
        }
    
    def draw_background_pattern(self):
        """Draw a subtle background pattern"""
        for i in range(0, self.width + 100, 100):
            for j in range(0, self.height + 100, 100):
                x = i + (self.animation_offset % 200) - 100
                y = j + (self.animation_offset % 200) - 100
                pygame.draw.circle(self.screen, (50, 50, 50), (x, y), 2)
    
    def draw_overlay(self):
        """Draw semi-transparent overlay"""
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
    
    def draw_stalemate_info(self):
        """Draw stalemate explanation and game info"""
        center_x = self.width // 2
        start_y = 150
        
        # Main title
        title_text = self.title_font.render("STALEMATE", True, self.gold)
        title_rect = title_text.get_rect(center=(center_x, start_y))
        self.screen.blit(title_text, title_rect)
        
        # Draw line under title
        line_y = start_y + 40
        pygame.draw.line(self.screen, self.gold, 
                        (center_x - 100, line_y), (center_x + 100, line_y), 3)
        
        # Game result
        result_text = self.subtitle_font.render("Game Drawn", True, self.white)
        result_rect = result_text.get_rect(center=(center_x, start_y + 70))
        self.screen.blit(result_text, result_rect)
        
        # Explanation
        explanation = [
            "No legal moves available",
            "King is not in check",
            "Result: Draw by stalemate"
        ]
        
        for i, line in enumerate(explanation):
            text = self.text_font.render(line, True, self.gray)
            text_rect = text.get_rect(center=(center_x, start_y + 120 + i * 30))
            self.screen.blit(text, text_rect)
    
    def draw_game_stats(self):
        """Draw game statistics"""
        center_x = self.width // 2
        stats_y = 400
        
        # Count pieces
        white_pieces = sum(len(self.board.pieces(piece_type, chess.WHITE)) 
                          for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, 
                                           chess.ROOK, chess.QUEEN, chess.KING])
        black_pieces = sum(len(self.board.pieces(piece_type, chess.BLACK)) 
                          for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, 
                                           chess.ROOK, chess.QUEEN, chess.KING])
        
        # Move count
        moves = self.board.fullmove_number
        
        stats = [
            f"Moves played: {moves}",
            f"White pieces: {white_pieces}",
            f"Black pieces: {black_pieces}",
            f"Turn: {'White' if self.board.turn else 'Black'}"
        ]
        
        for i, stat in enumerate(stats):
            text = self.text_font.render(stat, True, self.gray)
            text_rect = text.get_rect(center=(center_x, stats_y + i * 25))
            self.screen.blit(text, text_rect)
    
    def draw_buttons(self, mouse_pos):
        """Draw interactive buttons"""
        button_texts = {
            'new_game': 'New Game',
            'main_menu': 'Main Menu',
            'quit': 'Quit'
        }
        
        for button_name, rect in self.buttons.items():
            # Check if mouse is hovering
            is_hovering = rect.collidepoint(mouse_pos)
            button_color = self.button_hover if is_hovering else self.button_color
            
            # Draw button background
            pygame.draw.rect(self.screen, button_color, rect, border_radius=8)
            pygame.draw.rect(self.screen, self.gold, rect, width=2, border_radius=8)
            
            # Draw button text
            text = self.button_font.render(button_texts[button_name], True, self.button_text)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
            
            # Add glow effect if hovering
            if is_hovering:
                glow_rect = rect.inflate(4, 4)
                pygame.draw.rect(self.screen, self.gold + (100,), glow_rect, 
                               width=1, border_radius=10)
    
    def draw_decorative_elements(self):
        """Draw decorative chess-themed elements"""
        # Draw chess piece symbols in corners
        symbols = ['♔', '♕', '♖', '♗', '♘', '♙']
        corners = [
            (50, 50), (self.width - 50, 50),
            (50, self.height - 50), (self.width - 50, self.height - 50)
        ]
        
        for i, pos in enumerate(corners):
            if i < len(symbols):
                symbol = symbols[i]
                text = self.subtitle_font.render(symbol, True, (80, 80, 80))
                text_rect = text.get_rect(center=pos)
                self.screen.blit(text, text_rect)
    
    def handle_click(self, pos):
        """Handle mouse clicks on buttons"""
        for button_name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                return button_name
        return None
    
    def update_animation(self):
        """Update animation effects"""
        self.animation_offset += self.animation_speed
        if self.animation_offset > 400:
            self.animation_offset = 0
    
    def draw(self, mouse_pos):
        """Draw the complete stalemate screen"""
        # Clear screen with background pattern
        self.screen.fill(self.bg_color)
        self.draw_background_pattern()
        
        # Draw semi-transparent overlay
        self.draw_overlay()
        
        # Draw main content
        self.draw_stalemate_info()
        self.draw_game_stats()
        self.draw_decorative_elements()
        
        # Draw interactive elements
        self.draw_buttons(mouse_pos)
        
        # Update animations
        self.update_animation()


# Example usage in your main game loop
def show_stalemate_screen(screen, board):
    """Show the stalemate screen and handle events"""
    stalemate_screen = StalemateScreen(screen, board)
    clock = pygame.time.Clock()
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'main_menu'
                elif event.key == pygame.K_n:
                    return 'new_game'
                elif event.key == pygame.K_q:
                    return 'quit'
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    button_clicked = stalemate_screen.handle_click(mouse_pos)
                    if button_clicked:
                        return button_clicked
        
        # Draw the stalemate screen
        stalemate_screen.draw(mouse_pos)
        pygame.display.flip()
        clock.tick(60)
    
    return 'quit'


# Integration example for your main game
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Chess Game - Stalemate")
    
    # Example board in stalemate
    board = chess.Board("8/8/8/8/8/7k/6Q1/7K b - - 0 1")
    
    # Show stalemate screen
    result = show_stalemate_screen(screen, board)
    print(f"User chose: {result}")
    
    pygame.quit()