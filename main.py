from board import Board
from agent import MinimaxAgent

def play():
    board = Board()
    ai = MinimaxAgent("black", depth=3)

    while not board.is_game_over():
        board.print_board()
        move = input("Nhập nước đi của bạn (VD: e2e4): ")
        # TODO: Parse and apply player's move
        ai_move = ai.get_move(board)
        print("AI chọn:", ai_move)
        board.make_move(ai_move)

    print("Trò chơi kết thúc")

if __name__ == "__main__":
    play()
