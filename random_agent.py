import chess
import random


class RandomAgent:
    def __init__(self, color, board: chess.Board):
        self.color = color
        self.board = board

    def get_move(self):
        legal_moves = list(self.board.legal_moves)
        return random.choice(legal_moves)
        