from board import Board
piece_values = {
    "P": 100,
    "K": 320,
    "B": 330,
    "R": 500,
    "Q": 900,
    "K": 10000
}

SQUARES = [[f"{chr(ord('a') + col)}{8 - row}" for col in range(8)] for row in range(8)]

def evaluate(board, color):
    if board.is_game_over() :
        for row in range(len(board.board)):
            for col in range(len(board.board[row])):
                if board.board[row][col][1] == "K":
                    king_alive_color = 1 if board.board[row][col][0] == "w" else 0
        return 9999 if king_alive_color == color else -9999

    score = 0
    # Thêm điểm cho quân trắng hoặc đen kiểm soát trung tâm
    center_squares = ["c4" ,"d4", "e4", "f4", "c5" ,"d5", "e5", "f5"]
    for square in center_squares:
        if board.piece_at(square): 
            if board.piece_at(square)["color"] == color:
                score += 30 
    for row in SQUARES:
        for square in row:
            piece = board.piece_at(square)
            if piece:
                piece_value = piece_values.get(piece["piece_type"], 0)
                if piece["color"] == color:
                    score += piece_value
                else:
                    score -= piece_value

                # Thưởng cho việc phát triển quân
                if piece["piece_type"] in ["P" ,"K", "B"] and square not in defaultPosition(piece):
                    if piece["color"] == color:
                        score += 20 

    return score

def move_heuristic(board, move):
    score = 0
    piece_moving = board.piece_at(move[:2])
    captured_piece = board.piece_at(move[2:4])
    
    # Thưởng nếu là nước ăn quân
    if captured_piece:
        score += piece_values.get(captured_piece["piece_type"], 0)

    if piece_moving["piece_type"] in ["P" ,"K", "B"] and move[:2] not in defaultPosition(piece_moving):
        score += 20 

    board.make_move(move)

    # Thưởng nếu nước đi dẫn đến chiếu vua
    oppo_color = "black" if piece_moving["color"] else "white"
    if board.is_check(oppo_color):
        score += 150

    # Trừ điểm nếu vua di chuyển ra ngoài vùng an toàn
    if piece_moving["piece_type"] == "K":
        safe_squares = ["e1", "f1", "g1"] if piece_moving["color"] == 1 else ["e8", "f8", "g8"]
        if move[2:4] not in safe_squares:
            score -= 10
    board.undo_move(move)

    return score

def defaultPosition(piece):
    if piece["piece_type"] == "K":
        return ["b1", "g1"] if piece["color"] else ["b8", "g8"]
    elif piece["piece_type"] == "R":
        return ["a1", "h1"] if piece["color"] else ["a8", "h8"]
    elif piece["piece_type"] == "B":
        return ["c1", "f1"] if piece["color"] else ["c8", "f8"]
    elif piece["piece_type"] == "Q":
        return ["d1"] if piece["color"] else ["d8"]
    elif piece["piece_type"] == "K":
        return ["e1"] if piece["color"] else ["e8"]
    elif piece["piece_type"] == "P":
        return ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"
                    ] if piece["color"] else [
                "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"]
    else:
        return []