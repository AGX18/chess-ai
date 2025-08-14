# this will be a class where the ai player takes decision based on the minmax algorithm
# with alpha-beta pruning and iterative deepening 

# we want to max our score and minimize our opponent score (the other color)

# score is based on the piece and its rating
# ex.: we have a knight ,a bishop ,a queen and a king left but the other player have a rook and a pawn and a king
# then our score will be 3 + 3 + 9 + 12 - (5 + 1 + 12) = 9
# but if it's a checkmate then score will be inf it's against the other player
# and -inf if it's for us

# Score = (sum of our piece values) – (sum of opponent’s piece values)



import chess

class ChessAI:
    def __init__(self, ai_color, max_depth=4):
        self.ai_color = ai_color
        self.max_depth = max_depth
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 12
        }

    def evaluate(self, board):
        # Checkmate
        if board.is_checkmate():
            return float("inf") if board.turn != self.ai_color else -float("inf")
        # Draw
        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        score = 0
        for piece_type, value in self.piece_values.items():
            score += len(board.pieces(piece_type, self.ai_color)) * value
            score -= len(board.pieces(piece_type, not self.ai_color)) * value
        return score

    def get_move(self, board):
        """Returns the best move using Alpha-Beta pruning."""
        _, best_move = self.alpha_beta(board, self.max_depth, -float("inf"), float("inf"), board.turn == self.ai_color)
        return best_move

    def alpha_beta(self, board, depth, alpha, beta, maximizing):
        if depth == 0 or board.is_game_over():
            return self.evaluate(board), None

        best_move = None
        if maximizing:
            max_eval = -float("inf")
            for move in board.legal_moves:
                board.push(move)
                eval, _ = self.alpha_beta(board, depth - 1, alpha, beta, False)
                board.pop()

                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float("inf")
            for move in board.legal_moves:
                board.push(move)
                eval, _ = self.alpha_beta(board, depth - 1, alpha, beta, True)
                board.pop()

                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move
