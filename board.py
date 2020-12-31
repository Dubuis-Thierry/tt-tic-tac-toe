import pygame
import drawer
import misc
import random
from debuglogger import DebugLogger


def minimax(board, move, maximizing, turnx):
    board = board.copy()
    board.play(move)
    if board.game_result != "ongoing":
        return (["winner:O", "tie", "winner:X"].index(board.game_result)-1)*turnx
    
    if maximizing:
        value = -10e10
        for move in board.get_possible_moves():
            value = max(value, minimax(board, move, False, turnx))
        return value
    else:
        value = 10e10
        for move in board.get_possible_moves():
            value = min(value, minimax(board, move, True, turnx))
        return value


def find_best_move(board):
    """
    Given a board, what's the best move ?
    """
    if board.cells[board.dimensions//2][board.dimensions//2] == " ":
        return board.dimensions//2, board.dimensions//2
    turnx = 1 if board.turn % 2 == 0 else -1
    moves = {}
    for move in board.get_possible_moves():
        moves[move] = minimax(board, move, False, turnx)

    return max(moves.keys(), key=lambda x: moves[x])



class Board:
    def __init__(self, dimensions=3, ai=False, fake=False):
        self.dimensions = dimensions
        self.turn = 0  # even = circle, odd = cross
        self.game_result = "ongoing"
        self.cells = []
        if not fake:
            self.reset_cells()
        self.fake = fake
        self.ai = ai


    def copy(self):
        b = Board(self.dimensions, ai=False, fake=True)
        b.turn = self.turn
        b.game_result = self.game_result
        b.cells = [row.copy() for row in self.cells]
        return b
    

    def ai_move(self):
        if self.game_result == "ongoing":
            self.play(find_best_move(self), True)


    def get_player(self):
        return ['X', 'O'][self.turn%2]

    
    def get_possible_moves(self):
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                if cell == " ":
                    yield i, j
                    

    def print(self):
        for i in range(5 + 4 * (self.dimensions - 1)):
            print("-", end="")
        print()
        for row in self.cells:
            for i, cell in enumerate(row):
                print(f"| {cell} ", end="")
                if i == self.dimensions - 1:
                    print("|")
            for i in range(5 + 4 * (self.dimensions - 1)):
                print("-", end="")
            print()


    def win_check(self):
        # DIAGONALS
        s = self.cells[0][0]
        won = True
        if s != ' ':
            for i in range(self.dimensions):
                if self.cells[i][i] != s:
                    won = False
                    break
            if won:
                self.game_result = f"winner:{s}"
                if not self.fake:
                    DebugLogger.log("Game result determined with test #1")
                return
        
        s = self.cells[0][self.dimensions-1]
        won = True
        if s != ' ':
            for i in range(self.dimensions):
                if self.cells[i][self.dimensions-1-i] != s:
                    won = False
                    break
            if won:
                self.game_result = f"winner:{s}"
                if not self.fake:
                    DebugLogger.log("Game result determined with test #2")
                return
        
        # ROWS
        for i in range(self.dimensions):
            s = self.cells[i][0]
            if s != ' ':
                won = True
                for c in self.cells[i]:
                    if c != s:
                        won = False
                        break
                if won:
                    self.game_result = f"winner:{s}"
                    if not self.fake:
                        DebugLogger.log("Game result determined with test #3")
                    return
        
        # COLUMNS
        for i in range(self.dimensions):
            column = [self.cells[c][i] for c in range(self.dimensions)]
            s = column[0]
            if s != ' ':
                won = True
                for c in column:
                    if c != s:
                        won = False
                        break
                if won:
                    self.game_result = f"winner:{s}"
                    if not self.fake:
                        DebugLogger.log("Game result determined with test #4")
                    return
        if not " " in [self.cells[i][j] for i in range(self.dimensions) for j in range(self.dimensions)]:
            self.game_result = "tie"
            if not self.fake:
                DebugLogger.log("Game result determined with test #5")
            return
        self.game_result = "ongoing"
        return

    def reset_cells(self):
        self.cells = [
            [" " for i in range(self.dimensions)] for j in range(self.dimensions)
        ]
        self.game_result = "ongoing"
        self.turn = 0
    
    def play(self, target, ai_played=False):
        if self.game_result == "ongoing":
            i, j = target
            if (self.cells[i][j] == " "):
                if self.turn % 2 == 0: # CIRCLE
                    self.cells[i][j] = "X"
                else: # CROSS
                    self.cells[i][j] = "O"
                self.turn += 1
            
            self.win_check()
            if not self.fake:
                print(self.game_result)
                self.print()
            if self.ai and not ai_played:
                self.ai_move()




class PygameBoard(Board):
    def __init__(self, screen, rect, dimensions=3, ai=False):
        super().__init__(dimensions, ai)
        DebugLogger.log("Board __init__")
        self.screen = screen
        self.rect = rect
        self.x, self.y, self.width, self.height = rect

        self.w_width, self.w_height = screen.get_size()
        self.cell_size = self.width // self.dimensions

        self.lines_width = 4
        self.bg_color = (25, 20, 20)
        self.fg_color = (40, 150, 40)

        self.cross_color = (255, 0, 0)
        self.circle_color = (50, 50, 255)


        self.symbol_radius = self.cell_size // 3 + self.cell_size//4
        self.symbol_width = 8

        self.mouse_pressed = False

    
    def get_targetted(self, pos):
        x, y = pos

        x-=self.x
        y-=self.y

        x //= self.cell_size
        y //= self.cell_size

        return y, x
    

    def pygame_update(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.mouse_pressed:
                self.mouse_pressed = True
                if misc.is_in_rect(self.rect, pygame.mouse.get_pos()):
                    self.play(self.get_targetted(pygame.mouse.get_pos()))
        else:
            self.mouse_pressed = False
                
        self.pygame_draw()


    def pygame_draw(self):
        """
        Draws the board on screen in pygame
        """
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        # LINES
        for i in range(0, self.dimensions):
            # horizontal lines
            pygame.draw.line(
                self.screen, self.fg_color,
                (self.x, self.y + i*self.cell_size),
                (self.x + self.width, self.y + i*self.cell_size),
                self.lines_width
            )
            pygame.draw.line(
                self.screen, self.fg_color,
                (self.x, self.y + (i+1)*self.cell_size),
                (self.x + self.width, self.y + (i+1)*self.cell_size),
                self.lines_width
            )
            # vertical lines
            pygame.draw.line(
                self.screen, self.fg_color,
                (self.x + i * self.cell_size, self.y),
                (self.x + i * self.cell_size, self.y + self.height),
                self.lines_width
            )
            pygame.draw.line(
                self.screen, self.fg_color,
                (self.x + (i + 1) * self.cell_size, self.y),
                (self.x + (i + 1) * self.cell_size, self.y + self.height),
                self.lines_width
            )

            # Drawing symbols
            for i in range(self.dimensions):
                for j in range(self.dimensions):
                    center_pos = (self.x+self.cell_size//2+j*self.cell_size,
                            self.y+self.cell_size//2+i*self.cell_size)
                    if self.cells[i][j] == "X":
                        drawer.draw_cross(
                            self.screen,
                            center_pos,
                            self.symbol_radius,
                            self.cross_color,
                            self.symbol_width
                        )
                    elif self.cells[i][j] == "O":
                        pygame.draw.circle(
                            self.screen,
                            self.circle_color,
                            center_pos,
                            self.symbol_radius/2,
                            self.symbol_width
                        )


