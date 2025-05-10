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
    white_kings = sum(row.count("wK") for row in board.board)
    black_kings = sum(row.count("bK") for row in board.board)
    if white_kings == 0 and black_kings == 0:
        return "draw"
    if white_kings == 0:
        return "black"
    if black_kings == 0:
        return "white"
    return "draw"

def run_match(ai_agent, random_agent, rounds=10):
    # TODO: Chạy n ván đấu giữa AI và random agent, thống kê tỉ lệ thắng, đánh giá hiệu quả AI
    # Chạy n ván đấu giữa AI và random agent, thống kê tỉ lệ thắng, đánh giá hiệu quả AI
    results = []
    for _ in range(rounds):
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
