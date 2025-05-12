from board import Board
from agent import MinimaxAgent
from random_agent import RandomAgent
import time
import sys

def get_winner(board):
    """
    Xác định bên thắng dựa trên việc mất vua:
    - Mất cả hai vua -> draw
    - Mất vua trắng -> black thắng
    - Mất vua đen -> white thắng
    """
    white_king_exists = any("wK" in row for row in board.board)
    black_king_exists = any("bK" in row for row in board.board)
    
    if not white_king_exists and not black_king_exists:
        return "draw"
    if not white_king_exists:
        return "black"
    if not black_king_exists:
        return "white"
    
    current_color = "white" if len(board.move_history) % 2 == 0 else "black"
    if board.is_check(current_color):
        return "white" if current_color == "black" else "black"
    return "draw"


def run_match(ai_agent, random_agent, rounds=10):
    # TODO: Chạy n ván đấu giữa AI và random agent, thống kê tỉ lệ thắng, đánh giá hiệu quả AI
    # Chạy n ván đấu giữa AI và random agent, thống kê tỉ lệ thắng, đánh giá hiệu quả AI
    results = []
    for i in range(1, rounds + 1):
        print(f"Game {i}:")
        board = Board()
        current = "white"
        while not board.is_game_over():
            if current == ai_agent.color:
                move = ai_agent.get_move(board)
            else:
                move = random_agent.get_move(board)
            if move is None:
                break
            board.make_move(move)
            current = "black" if current == "white" else "white"

        winner = get_winner(board)
        if winner == ai_agent.color:
            results.append("win")
        elif winner == random_agent.color:
            results.append("lose")
        else:
            results.append("draw")
        print(f"Game {i}: {winner.upper()} wins." if winner in ["white", "black"] else f"Game {i}: Draw.")
    wins = results.count("win")
    return wins

if __name__ == "__main__":
    ROUNDS = 10
    ai = MinimaxAgent("white", depth=3)
    rnd = RandomAgent("black")
    wins = run_match(ai, rnd, ROUNDS)

    print(f"AI đã thắng {wins}/{ROUNDS} ván.")
    if wins == ROUNDS:
        print("Kết quả: PASS")
        sys.exit(0)
    else:
        print("Kết quả: FAIL")
        sys.exit(1)
