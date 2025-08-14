import chess

class ChessAI:
    def __init__(self, ai_color, board, max_depth=4):
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

    def evaluate(self):
        """Evaluate from AI's perspective: higher = better for AI."""
        if self.board.is_checkmate():
            return -float("inf") if self.board.turn == self.ai_color else float("inf")
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0

        score = 0
        for piece_type, value in self.piece_values.items():
            score += len(self.board.pieces(piece_type, self.ai_color)) * value
            score -= len(self.board.pieces(piece_type, not self.ai_color)) * value

        # If AI is black, flip score so positive = good for AI
        if self.ai_color == chess.BLACK:
            score = -score

        return score

    def order_moves(self, moves):
        """Prioritize captures to improve pruning."""
        def score_move(move):
            if self.board.is_capture(move):
                captured = self.board.piece_at(move.to_square)
                attacker = self.board.piece_at(move.from_square)
                return 10 * (captured.piece_type if captured else 0) - attacker.piece_type
            return 0
        return sorted(moves, key=score_move, reverse=True)

    def negamax(self, depth, alpha, beta):
        """
        Negamax: always returns score from AI's perspective.
        No 'maximizing' flag needed.
        """
        if depth == 0 or self.board.is_game_over():
            return self.evaluate()

        best_score = -float("inf")
        best_move = None
        alpha_orig = alpha

        moves = self.order_moves(list(self.board.legal_moves))
        for move in moves:
            self.board.push(move)
            score = -self.negamax(depth - 1, -beta, -alpha)  # Flip score
            self.board.pop()

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, score)
            if alpha >= beta:  # Beta cutoff
                break

        # At root, return best move
        if depth == self.max_depth:
            self.best_root_move = best_move

        return best_score

    def get_move(self):
        """Use iterative deepening to find best move."""
        best_move = None

        legal_moves = list(self.board.legal_moves)
        if len(legal_moves) == 0:
            return None
        if len(legal_moves) == 1:
            return legal_moves[0]

        # Iterative deepening
        for depth in range(1, self.max_depth + 1):
            self.best_root_move = None
            score = self.negamax(depth, -float("inf"), float("inf"))
            if self.best_root_move:
                best_move = self.best_root_move
            print(f"Depth {depth}: {best_move} (score: {score})")

        return best_move