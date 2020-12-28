import pygame
import drawer
import misc
import random

from debuglogger import DebugLogger

class Board:
    def __init__(self, screen, rect, dimensions=3):
        DebugLogger.log("Board __init__")
        self.screen = screen
        self.rect = rect
        self.x, self.y, self.width, self.height = rect

        self.dimensions = dimensions

        self.w_width, self.w_height = screen.get_size()
        self.cell_size = self.width // self.dimensions

        self.lines_width = 4
        self.bg_color = (25, 20, 20)
        self.fg_color = (40, 150, 40)

        self.cross_color = (255, 0, 0)
        self.circle_color = (50, 50, 255)


        self.symbol_radius = self.cell_size // 3 + self.cell_size//4
        self.symbol_width = 8

        self.turn = 0  # even = circle, odd = cross

        self.mouse_pressed = False

        self.game_result = "ongoing"
        self.cells = []
        self.reset_cells()
    

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
                    DebugLogger.log("Game result determined with test #4")
                    return
        if not " " in [self.cells[i][j] for i in range(self.dimensions) for j in range(self.dimensions)]:
            self.game_result = "tie"
            DebugLogger.log("Game result determined with test #5")
            return
        self.game_result = "ongoing"
        return

    def reset_cells(self):
        self.cells = [
            [" " for i in range(self.dimensions)] for j in range(self.dimensions)
        ]
        self.game_result = "ongoing"
        self.turn = random.randint(0, 1)
        DebugLogger.log("Board set for new game")
    
    def play(self, target):
        if self.game_result == "ongoing":
            i, j = target
            if (self.cells[i][j] == " "):
                if self.turn % 2 == 0: # CIRCLE
                    self.cells[i][j] = "O"
                else: # CROSS
                    self.cells[i][j] = "X"
                self.turn += 1
            
            self.win_check()

            print(self.game_result)
            
    
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


