import pygame
import time
from board import Board
from agent import MinimaxAgent

WIDTH, HEIGHT = 700, 740
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
GRAY = (128, 128, 128, 120)
BLACK = (0, 0, 0)

class ChessGUI:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess AI GUI")
        self.board = Board()
        self.selected = None
        self.legal_moves_for_selected = []
        self.running = True
        self.human_color = "white"
        self.depth = None
        self.ai = None
        self.load_images()
        self.font = pygame.font.SysFont("arial", 20)
        self.difficulty_selected = False
        self.undo_used = False
        self.turn_time = 60
        self.last_tick = pygame.time.get_ticks()
        self.status_msg = ""

    def load_images(self):
        self.pieces = {}
        for piece in ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK',
                      'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']:
            self.pieces[piece] = pygame.transform.scale(
                pygame.image.load(f"assets/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE)
            )

    def draw_difficulty_menu(self):
        self.win.fill((200, 200, 200))
        title = self.font.render("Choose difficulty:", True, BLACK)
        self.win.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 120))
        easy = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 - 60, 120, 40)
        medium = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2, 120, 40)
        hard = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 60, 120, 40)
        pygame.draw.rect(self.win, (100, 200, 100), easy)
        pygame.draw.rect(self.win, (100, 100, 200), medium)
        pygame.draw.rect(self.win, (200, 100, 100), hard)
        easy_text = self.font.render("Easy", True, BLACK)
        medium_text = self.font.render("Medium", True, BLACK)
        hard_text = self.font.render("Difficult", True, BLACK)
        self.win.blit(easy_text, (easy.centerx - easy_text.get_width() // 2, easy.centery - easy_text.get_height() // 2))
        self.win.blit(medium_text, (medium.centerx - medium_text.get_width() // 2, medium.centery - medium_text.get_height() // 2))
        self.win.blit(hard_text, (hard.centerx - hard_text.get_width() // 2, hard.centery - hard_text.get_height() // 2))
        pygame.display.flip()
        return easy, medium, hard

    def waiting_ending(self,ending_msg,under_msg):
        self.win.fill((200, 200, 200))
        title = self.font.render(ending_msg, True, BLACK)
        self.win.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 120))
        under = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 - 60, 120, 40)
        pygame.draw.rect(self.win, (100, 200, 100), under)
        self.win.blit(under_msg, (under.centerx - under_msg.get_width() // 2, under.centery - under_msg.get_height() // 2))
        pygame.display.flip()

    def draw_board(self):
        pygame.draw.rect(self.win, (240, 240, 240), (0, 0, WIDTH, 40))
        pygame.draw.rect(self.win, (200, 0, 0), (WIDTH - 100, 5, 80, 30))
        undo_text = self.font.render("Undo", True, (255, 255, 255))
        self.win.blit(undo_text, (WIDTH - 85, 10))

        countdown_text = self.font.render(f"Time left: {int(self.turn_time)}s", True, BLACK)
        self.win.blit(countdown_text, (10, 10))

        # Display status message
        if self.status_msg:
            status_text = self.font.render(self.status_msg, True, BLACK)
            self.win.blit(status_text, (WIDTH // 2 - status_text.get_width() // 2, 10))

        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BROWN
                pygame.draw.rect(self.win, color, (col*SQUARE_SIZE, row*SQUARE_SIZE + 40, SQUARE_SIZE, SQUARE_SIZE))

        if self.selected and self.legal_moves_for_selected:
            for r, c in self.legal_moves_for_selected:
                s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                s.fill(GRAY)
                self.win.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE + 40))

    def draw_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.get_piece_at(row, col)
                if piece != "--" and piece in self.pieces:
                    x = col * SQUARE_SIZE
                    y = row * SQUARE_SIZE + 40
                    self.win.blit(self.pieces[piece], (x, y))

    def get_clicked_square(self, pos):
        x, y = pos
        if WIDTH - 100 <= x <= WIDTH - 20 and 5 <= y <= 35:
            return "undo"
        if y < 40:
            return None
        col = x // SQUARE_SIZE
        row = (y - 40) // SQUARE_SIZE
        return row, col

    def show_message(self, message):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.win.blit(overlay, (0, 0))
        text = self.font.render(message, True, (255, 255, 255))
        self.win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        time.sleep(3)

    def highlight_positions(self, positions, color):
        for row, col in positions:
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill((*color, 120))
            self.win.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE + 40))

    def wait_for_exit(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

    def run(self):
        clock = pygame.time.Clock()
        player_turn = self.human_color

        while not self.difficulty_selected:
            easy, medium, hard = self.draw_difficulty_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if easy.collidepoint(event.pos):
                        self.depth = 1
                        self.difficulty_selected = True
                    elif medium.collidepoint(event.pos):
                        self.depth = 3
                        self.difficulty_selected = True
                    elif hard.collidepoint(event.pos):
                        self.depth = 5
                        self.difficulty_selected = True

        self.ai = MinimaxAgent("black", depth=self.depth)

        while self.running:
            now = pygame.time.get_ticks()
            delta = (now - self.last_tick) / 1000
            self.last_tick = now

            if player_turn == self.human_color:
                self.turn_time -= delta
                if self.turn_time <= 0:
                    print("⏱ Time's up! Skipping turn.")
                    player_turn = self.ai.color
                    self.selected = None
                    self.legal_moves_for_selected = []
                    self.turn_time = 60
                    self.undo_used = False

            clock.tick(60)
            self.win.fill((0, 0, 0))
            self.draw_board()
            self.draw_pieces()

            # Check game state
            if self.board.is_game_over():
                if self.board.is_check(player_turn):
                    winner = "black" if player_turn == "white" else "white"
                    under_msg = "Black is checkmated!" if player_turn == "white" else "White is checkmated!"
                    if winner == self.human_color:
                        ending_msg = "You Win"
                    else:
                        ending_msg = "You Lose"
                else:
                    ending_msg = "Stalemate! It's a draw."
                continue
            elif self.board.is_check(player_turn):
                king_pos = self.board.get_king_position(player_turn)
                self.highlight_positions([king_pos], (255, 0, 0))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and player_turn == self.human_color:
                    result = self.get_clicked_square(pygame.mouse.get_pos())
                    if result == "undo":
                        if self.undo_used and len(self.board.move_history) >= 2:
                            self.board.undo_move(ai_move)
                            self.board.undo_move(move_str)
                            player_turn = self.human_color
                            self.selected = None
                            self.legal_moves_for_selected = []
                            self.turn_time = 60
                            self.undo_used = False
                        continue
                    elif result is None:
                        continue
                    row, col = result
                    if self.selected:
                        from_row, from_col = self.selected
                        if (row, col) in self.legal_moves_for_selected:
                            move_str = self.coords_to_move_str(from_row, from_col, row, col)
                            self.board.make_move(move_str)
                            self.undo_used = True
                            player_turn = self.ai.color
                            self.turn_time = 60
                        self.selected = None
                        self.legal_moves_for_selected = []
                    else:
                        piece = self.board.get_piece_at(row, col)
                        if piece.startswith(self.human_color[0]):
                            self.selected = (row, col)
                            legal_moves_str = self.board.get_legal_moves_at(row, col)
                            self.legal_moves_for_selected = []
                            for move in legal_moves_str:
                                end_col = ord(move[2]) - ord('a')
                                end_row = 8 - int(move[3])
                                self.legal_moves_for_selected.append((end_row, end_col))

            if player_turn == self.ai.color:
                ai_move = self.ai.get_move(self.board)
                if ai_move:
                    self.board.make_move(ai_move)
                    player_turn = self.human_color
                    self.turn_time = 60

        while True:
            self.waiting_ending(ending_msg, under_msg)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

    def coords_to_move_str(self, r1, c1, r2, c2):
        return (
            chr(c1 + ord('a')) + str(8 - r1) +
            chr(c2 + ord('a')) + str(8 - r2)
        )

if __name__ == "__main__":
    gui = ChessGUI()
    gui.run()
