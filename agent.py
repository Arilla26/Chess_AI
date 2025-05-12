from heuristic import evaluate, move_heuristic
from board import Board

class MinimaxAgent:
    def __init__(self, color, depth=3, use_alpha_beta=True):
        self.color = color
        self.depth = depth
        self.use_alpha_beta = use_alpha_beta

    def get_move(self, board):
        if self.depth == 0 or board.is_game_over():
            color = 1 if self.color == "white" else 0
            return evaluate(board, color)
        alpha = float("-inf")
        beta = float("inf")
        bestMove = None

        legalMoves = list(board.get_legal_moves(self.color))
        legalMoves = sorted(legalMoves, key=lambda m: move_heuristic(board, m), reverse=1)
        for move in legalMoves:
            board.make_move(move)
            eval = self.minimax(board, 1, self.depth, alpha, beta, False)
            board.undo_move(move)
            if eval > alpha:
                alpha = eval
                bestMove = move
        return bestMove

    def minimax(self, board, depth, depthMax, alpha, beta, maximizing):
        if depth == depthMax or board.is_game_over():
            color = 1 if self.color == "white" else 0
            return evaluate(board, color)
        
        if maximizing:
            legalMoves = list(board.get_legal_moves(self.color))
            if depth <= -(-depthMax // 2):
                legalMoves = sorted(legalMoves, key=lambda m: move_heuristic(board, m), reverse = 1)
            maxEval = float("-inf")
            for move in legalMoves:
                board.make_move(move)
                eval = self.minimax(board, depth+1, depthMax, alpha, beta, False)
                board.undo_move(move)
                maxEval = max(maxEval,eval)
                alpha = max(alpha,eval)
                if self.use_alpha_beta and alpha >= beta:
                    break
            return maxEval
        else:
            opposite_color = "white" if self.color == "black" else "black"
            legalMoves = list(board.get_legal_moves(opposite_color))
            if depth <= -(-depthMax // 2):
                legalMoves = sorted(legalMoves, key=lambda m: move_heuristic(board, m), reverse = 0)
            minEval = float("inf")
            for move in legalMoves:
                board.make_move(move)
                eval = self.minimax(board, depth+1, depthMax, alpha, beta, True)
                board.undo_move(move)
                minEval = min(minEval,eval)
                beta = min(beta,eval)
                if self.use_alpha_beta and alpha >= beta:
                    break
            return minEval
