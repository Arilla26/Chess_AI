class Board:
    def __init__(self):
        ### Khởi tạo bàn cờ 8x8 với vị trí các quân ban đầu
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.move_history = []
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rook_moved = {"h1": False, "a1": False}
        self.black_rook_moved = {"h8": False, "a8": False}
        self.en_passant_target = None
        self.castling_rights = {
            "white_kingside": True,
            "white_queenside": True,
            "black_kingside": True,
            "black_queenside": True
        }

    def get_legal_moves(self, color):
        move_gen = MoveGenerator(self.board, color, self)
        pseudo_moves = move_gen.get_legal_moves(color)
        legal_moves = []
        for move in pseudo_moves:
            board_copy = self.clone()
            board_copy.make_move(move)
            if not board_copy.is_check(color):
                legal_moves.append(move)
        return legal_moves

    def coord_to_pos(self, r, c):
        return chr(c + ord('a')) + str(8 - r)

    def get_legal_moves_at(self, row, col):
        """
        Trả về danh sách nước đi hợp lệ (string) bắt đầu từ vị trí (row, col)
        """
        start_pos = self.coord_to_pos(row, col)
        piece = self.get_piece_at(row, col)
        if piece == "--":
            return []
        color = "white" if piece.startswith("w") else "black"
        all_moves = self.get_legal_moves(color)
        filtered = [move for move in all_moves if move.startswith(start_pos)]
        return filtered

    def make_move(self, move):
        start_col = ord(move[0]) - ord('a')
        start_row = 8 - int(move[1])
        end_col = ord(move[2]) - ord('a')
        end_row = 8 - int(move[3])
        piece = self.board[start_row][start_col]
        captured = self.board[end_row][end_col]
        # Castling
        if piece[1] == 'K' and abs(end_col - start_col) == 2:
            if end_col > start_col:
                self.board[end_row][5] = self.board[end_row][7]
                self.board[end_row][7] = "--"
            else:
                self.board[end_row][3] = self.board[end_row][0]
                self.board[end_row][0] = "--"
        # En Passant
        if piece[1] == 'P' and (end_col != start_col and captured == "--"):
            captured = "--"
            self.board[start_row][end_col] = "--"
        self.move_history.append((move, piece, captured, self.en_passant_target))
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = "--"
        # Promotion
        if piece[1] == 'P' and (end_row == 0 or end_row == 7):
            self.board[end_row][end_col] = piece[0] + 'Q'
        # Update en passant target
        if piece[1] == 'P' and abs(end_row - start_row) == 2:
            self.en_passant_target = ((start_row + end_row) // 2, start_col)
        else:
            self.en_passant_target = None
        if piece == 'wK':
            self.white_king_moved = True
            self.castling_rights['white_kingside'] = False
            self.castling_rights['white_queenside'] = False
        if piece == 'bK':
            self.black_king_moved = True
            self.castling_rights['black_kingside'] = False
            self.castling_rights['black_queenside'] = False
        if piece == 'wR' and move[:2] == 'h1':
            self.white_rook_moved['h1'] = True
            self.castling_rights['white_kingside'] = False
        if piece == 'wR' and move[:2] == 'a1':
            self.white_rook_moved['a1'] = True
            self.castling_rights['white_queenside'] = False
        if piece == 'bR' and move[:2] == 'h8':
            self.black_rook_moved['h8'] = True
            self.castling_rights['black_kingside'] = False
        if piece == 'bR' and move[:2] == 'a8':
            self.black_rook_moved['a8'] = True
            self.castling_rights['black_queenside'] = False

    def undo_move(self, move):
        if not self.move_history:
            return
        last_move, piece, captured, prev_en_passant = self.move_history.pop()
        start_col = ord(move[0]) - ord('a')
        start_row = 8 - int(move[1])
        end_col = ord(move[2]) - ord('a')
        end_row = 8 - int(move[3])
        # Undo promotion
        if piece[1] == 'P' and (end_row == 0 or end_row == 7) and self.board[end_row][end_col][1] == 'Q':
            self.board[end_row][end_col] = piece[0] + 'P'
        self.board[start_row][start_col] = piece
        # Undo en passant
        if piece[1] == 'P' and end_col != start_col and captured == "--":
            self.board[end_row][end_col] = "--"
            self.board[start_row][end_col] = 'bP' if piece[0] == 'w' else 'wP'
        else:
            self.board[end_row][end_col] = captured
        # Undo castling
        if piece[1] == 'K' and abs(end_col - start_col) == 2:
            if end_col > start_col:
                self.board[end_row][7] = self.board[end_row][5]
                self.board[end_row][5] = "--"
            else:
                self.board[end_row][0] = self.board[end_row][3]
                self.board[end_row][3] = "--"
        self.en_passant_target = prev_en_passant

    def is_game_over(self):
        white_king_exists = False
        black_king_exists = False
        for row in self.board:
            for piece in row:
                if piece == "wK":
                    white_king_exists = True
                elif piece == "bK":
                    black_king_exists = True
        if not white_king_exists or not black_king_exists:
            return True  # Một bên mất vua
        current_color = "white" if len(self.move_history) % 2 == 0 else "black"
        legal_moves = self.get_legal_moves(current_color)
        if not legal_moves:
            if self.is_check(current_color):
                print(f"Checkmate! {current_color} bị chiếu hết.")
                return True
            else:
                print("Stalemate! Hòa do không còn nước đi hợp lệ.")
                return True
        return False

    def get_piece_at(self, row, col):
        return self.board[row][col]

    def piece_at(self, square):
        column_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                      'e': 4, 'f': 5, 'g': 6, 'h': 7}
        piece = self.get_piece_at(8 - int(square[1]), column_map[square[0]])
        if piece != "--":
            color = 1 if piece[0] == 'w' else 0
            piece_type = piece[1]
            return {"color": color, "piece_type": piece_type}
        else:
            return None

    def clone(self):
        new_board = Board()
        new_board.board = [row[:] for row in self.board]
        new_board.move_history = self.move_history[:]
        new_board.white_king_moved = self.white_king_moved
        new_board.black_king_moved = self.black_king_moved
        new_board.white_rook_moved = self.white_rook_moved.copy()
        new_board.black_rook_moved = self.black_rook_moved.copy()
        new_board.en_passant_target = self.en_passant_target
        new_board.castling_rights = self.castling_rights.copy()
        return new_board

    def is_check(self, color):
        enemy_color = "black" if color == "white" else "white"
        king_pos = None
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece == ("wK" if color == "white" else "bK"):
                    king_pos = (r, c)
                    break
            if king_pos:
                break
        if king_pos is None:
            return False
        move_gen = MoveGenerator(self.board, enemy_color, self)
        enemy_moves = move_gen.get_legal_moves(enemy_color)
        king_square = self.coord_to_pos(*king_pos)
        for move in enemy_moves:
            if move[2:4] == king_square:
                return True
        return False

    def get_king_position(self, color):
        king = "wK" if color == "white" else "bK"
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == king:
                    return row, col
        return None

    def get_attacking_pieces(self, color):
        king_pos = self.get_king_position(color)
        if not king_pos:
            return []
        attacking_pieces = []
        move_gen = MoveGenerator(self.board, "black" if color == "white" else "white", self)
        for move in move_gen.get_legal_moves("black" if color == "white" else "white"):
            end_row, end_col = 8 - int(move[3]), ord(move[2]) - ord('a')
            if (end_row, end_col) == king_pos:
                start_row, start_col = 8 - int(move[1]), ord(move[0]) - ord('a')
                attacking_pieces.append((start_row, start_col))
        return attacking_pieces

    def print_board(self):
        for row in self.board:
            print(" ".join(row))
        print()

class MoveGenerator:
    def __init__(self, board, color, board_obj):
        self.board = board
        self.color = color
        self.board_obj = board_obj

    def get_legal_moves(self, color):
        self.color = color
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece.startswith(color[0]):
                    piece_type = piece[1]
                    match piece_type:
                        case 'P':
                            moves.extend(self._pawn_moves(row, col, color))
                        case 'N':
                            moves.extend(self._knight_moves(row, col, color))
                        case 'B':
                            moves.extend(self._bishop_moves(row, col, color))
                        case 'R':
                            moves.extend(self._rook_moves(row, col, color))
                        case 'Q':
                            moves.extend(self._queen_moves(row, col, color))
                        case 'K':
                            moves.extend(self._king_moves(row, col, color))
        return moves

    def _pawn_moves(self, row, col, color):
        moves = []
        direction = -1 if color == "white" else 1
        start_row = 6 if color == "white" else 1
        enemy_color = 'b' if color == 'white' else 'w'
        # Move 1 square
        if 0 <= row + direction < 8 and self.board[row + direction][col] == "--":
            if row + direction == 0 or row + direction == 7:
                for promo in ['q', 'r', 'b', 'n']:
                    moves.append(self._move_str(row, col, row + direction, col, promo))
            else:
                moves.append(self._move_str(row, col, row + direction, col))
            if row == start_row and self.board[row + 2 * direction][col] == "--":
                moves.append(self._move_str(row, col, row + 2 * direction, col))
        # Capture left/right
        for dc in [-1, 1]:
            new_row, new_col = row + direction, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target.startswith(enemy_color):
                    if new_row == 0 or new_row == 7:
                        for promo in ['q', 'r', 'b', 'n']:
                            moves.append(self._move_str(row, col, new_row, new_col, promo))
                    else:
                        moves.append(self._move_str(row, col, new_row, new_col))
        # En passant
        ep_target = self.board_obj.en_passant_target
        if ep_target:
            ep_row, ep_col = ep_target
            if row == (3 if color == "white" else 4) and abs(col - ep_col) == 1:
                if ep_row == row + direction:
                    moves.append(self._move_str(row, col, ep_row, ep_col))
        return moves

    def _knight_moves(self, row, col, color):
        moves = []
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                      (1, -2), (1, 2), (2, -1), (2, 1)]
        own_color = 'w' if color == 'white' else 'b'
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = self.board[r][c]
                if target == "--" or not target.startswith(own_color):
                    moves.append(self._move_str(row, col, r, c))
        return moves

    def _bishop_moves(self, row, col, color):
        return self._slide_moves(row, col, color, [(-1, -1), (-1, 1), (1, -1), (1, 1)])

    def _rook_moves(self, row, col, color):
        return self._slide_moves(row, col, color, [(-1, 0), (1, 0), (0, -1), (0, 1)])

    def _queen_moves(self, row, col, color):
        return self._slide_moves(row, col, color, [(-1, -1), (-1, 0), (-1, 1),
                                                  (0, -1),           (0, 1),
                                                  (1, -1),  (1, 0),  (1, 1)])

    def _king_moves(self, row, col, color):
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
        own_color = 'w' if color == 'white' else 'b'
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = self.board[r][c]
                if target == "--" or not target.startswith(own_color):
                    moves.append(self._move_str(row, col, r, c))
        # Castling
        if color == 'white' and row == 7 and col == 4:
            if self.board_obj.castling_rights['white_kingside']:
                if self.board[7][5] == "--" and self.board[7][6] == "--":
                    moves.append("e1g1")
            if self.board_obj.castling_rights['white_queenside']:
                if self.board[7][1] == "--" and self.board[7][2] == "--" and self.board[7][3] == "--":
                    moves.append("e1c1")
        elif color == 'black' and row == 0 and col == 4:
            if self.board_obj.castling_rights['black_kingside']:
                if self.board[0][5] == "--" and self.board[0][6] == "--":
                    moves.append("e8g8")
            if self.board_obj.castling_rights['black_queenside']:
                if self.board[0][1] == "--" and self.board[0][2] == "--" and self.board[0][3] == "--":
                    moves.append("e8c8")
        return moves

    def _slide_moves(self, row, col, color, directions):
        moves = []
        own_color = 'w' if color == 'white' else 'b'
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = self.board[r][c]
                if target == "--":
                    moves.append(self._move_str(row, col, r, c))
                elif target.startswith(own_color):
                    break
                else:
                    moves.append(self._move_str(row, col, r, c))
                    break
                r += dr
                c += dc
        return moves

    def _move_str(self, start_row, start_col, end_row, end_col, promotion=None):
        move = (chr(ord('a') + start_col) + str(8 - start_row) +
                chr(ord('a') + end_col) + str(8 - end_row))
        if promotion:
            move += promotion
        return move
