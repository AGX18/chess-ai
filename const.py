# Screen Dimensions
WIDTH = 800
HEIGHT = 800

# Board Dimensions
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE

LIGHT_SQUARE = (234, 235, 200)  # Light brown
DARK_SQUARE = (119, 154, 88)    # Dark brown

normal_pieces = "imgs-80px"
clicked_pieces = "imgs-128px"
pieces = ['wK', 'wQ', 'wR', 'wB', 'wN', 'wP',
          'bK', 'bQ', 'bR', 'bB', 'bN', 'bP']


highlighted_squares_light = "#C86464"
highlighted_squares_dark = "#C84646"



# for setup screen
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 200, 0)
BLUE = (50, 150, 255)
RED = (200, 50, 50)
DARK_GRAY = (40, 40, 40)
HIGHLIGHT = (0, 180, 255)

# Options: 0 = Human, 1 = AI

# Player options
player_types = ["Human", "AI", "Random"]
white_choice = 0  # Human
black_choice = 0  # Human
ai_depth = 4  # Default depth for AI (random & human ignore this)

# Button dimensions
button_width, button_height = 140, 50
gap = 25


# Button dimensions
button_width, button_height = 120, 50
gap = 20
