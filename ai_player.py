import chess
import random

class ChessAI:
    def __init__(self, ai_color, board : chess.Board, max_depth=4):
        self.board = board
        self.ai_color = ai_color
        self.max_depth = max_depth
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0  # Never use high king value!
        }
        self.best_move = None

    def get_move(self):
        self.maximize(self.max_depth, -float('inf'), float('inf'))
        if self.best_move == None:
            legal_moves = list(self.board.legal_moves)
            if not legal_moves:
                print("No legal moves!")
                return None
            self.best_move = random.choice(legal_moves)
        best_move = self.best_move
        self.best_move = None
        return best_move

    def maximize(self, depth, alpha, beta) -> float:
        if depth == 0:
            return self.get_board_rating()
        
        legal_moves = list(self.board.legal_moves)

        for move in legal_moves:
            self.board.push(move)
            rating = self.minimize(depth - 1, alpha, beta)
            self.board.pop()

            if rating > alpha:
                alpha = rating
                if depth == self.max_depth:
                    self.best_move = move

            if alpha >= beta:
                break
        
        return alpha


    def minimize(self, depth, alpha, beta) -> float:
        # TODO: implement minimize in alpha beta prunning algorithm
        if depth == 0:
            return self.get_board_rating()
        
        legal_moves = self.board.legal_moves

        for move in legal_moves:
            self.board.push(move)
            rating = self.maximize(depth - 1, alpha, beta)
            self.board.pop()

            if rating < beta:
                beta = rating

            if beta <= alpha:
                break                    
        
        return beta
    
    def get_board_rating(self):
        my_score  = 0
        opponent_score  = 0
        for piece_type, value in self.piece_values.items():
            my_score += len(self.board.pieces(piece_type, self.ai_color)) * value
            opponent_score += len(self.board.pieces(piece_type, not self.ai_color)) * value

        noise = random.uniform(-0.1, 0.1)
        if self.board.is_repetition(3):
            my_score -= 0.5  # discourage repeating positions
        return my_score - opponent_score + noise
