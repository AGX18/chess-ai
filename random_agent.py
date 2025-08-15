import chess
import random
import time

class RandomAgent:
    def __init__(self, color, board: chess.Board):
        self.color = color
        self.board = board

    def get_move(self):
        start_time = time.time()
        legal_moves = list(self.board.legal_moves)
        choice = random.choice(legal_moves)
        self.logging(start_time)
        return choice 
        
    def logging(self, start_time):
        end_time = time.time()

        # Calculate difference
        elapsed_time = end_time - start_time
        print("White" if self.board.turn == chess.WHITE else "Black")
        print(f"time needed for random agent: {elapsed_time:.4f} seconds")