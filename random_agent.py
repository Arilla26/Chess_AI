import random

class RandomAgent:
    def __init__(self, color):
        self.color = color

    def get_move(self, board):
        # TODO: Chọn ngẫu nhiên một nước đi hợp lệ cho màu mình điều khiển – không tính toán gì
        legal_moves = board.get_legal_moves(self.color)
        if not legal_moves:
            return None
        return random.choice(legal_moves)
