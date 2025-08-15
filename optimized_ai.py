from ai_player import ChessAI
import chess
import time
class OptimizedAI(ChessAI):
    def __init__(self, ai_color, board : chess.Board, max_depth=4):
        super().__init__(ai_color, board, max_depth)
        self.killer_moves = [[None, None] for _ in range(max_depth + 1)]
        # History heuristic: history[from_square][to_square]
        self.history = [[0] * 64 for _ in range(64)]  # 64 squares
    
    def order_moves(self):
        """
        Returns a list of moves sorted by estimated value (best first).
        """
        board = self.board
        depth = self.max_depth
        moves = list(board.legal_moves)
        scored_moves = []

        for move in moves:
            score = 0

            # 1. PV Move: Not implemented here (needs transposition table)
            # 2. Captures with MVV-LVA
            if board.is_capture(move):
                captured = board.piece_at(move.to_square)
                attacker = board.piece_at(move.from_square)
                # MVV-LVA: high value captured, low value attacker → better
                if captured and attacker:
                    score += 10 * (captured.piece_type if captured else 0) - attacker.piece_type
                    score += 1000  # Base capture bonus


            # 4. Killer Moves
            if self.killer_moves[depth][0] == move:
                score += 8000
            elif self.killer_moves[depth][1] == move:
                score += 7000

            # 5. History Heuristic
            score += self.history[move.from_square][move.to_square]

            # 6. Check
            board.push(move)
            if board.is_check():
                score += 200
            board.pop()

            scored_moves.append((score, move))

        # Sort by score, descending
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        return [move for score, move in scored_moves]
    
    def maximize(self, depth, alpha, beta) -> float:
        if depth == 0:
            return self.get_board_rating()
        
        legal_moves = self.order_moves()

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
        
        legal_moves = self.order_moves()

        for move in legal_moves:
            self.board.push(move)
            rating = self.maximize(depth - 1, alpha, beta)
            self.board.pop()

            if rating < beta:
                beta = rating

            if beta <= alpha:
                break                    
        
        return beta
    

    
    def logging(self, start_time):
        end_time = time.time()

        # Calculate difference
        elapsed_time = end_time - start_time
        print("White" if self.board.turn == chess.WHITE else "Black")
        print(f"time needed for ai with move ordering: {elapsed_time:.4f} seconds")
    


        