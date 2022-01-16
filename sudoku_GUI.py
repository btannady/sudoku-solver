"""
sudoku_GUI.py

establishes/maintains GUI, allowing users to play or auto-solve sudoku grids
"""

import pygame
import time
from sudoku_solver import solve_sudoku, is_valid_num, find_empty_space
pygame.font.init()

# ========================================================
# sets up sudoku GUI, translates user input to GUI actions, and updates cube cell data to GUI 
class Grid:
    
    board = [
        [7, 0, 8, 0, 3, 0, 0, 1, 0],
        [0, 1, 9, 0, 6, 8, 5, 0, 2], 
        [0, 0, 0, 0, 0, 4, 3, 0, 0],
        [0, 5, 6, 3, 7, 0, 0, 0, 1],
        [0, 0, 1, 8, 0, 0, 0, 9, 5],
        [0, 9, 0, 0, 2, 0, 6, 0, 0],
        [1, 0, 3, 4, 0, 7, 2, 0, 0],
        [5, 0, 0, 2, 0, 0, 0, 0, 8],
        [0, 8, 0, 0, 0, 1, 4, 7, 0]]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, num_candidate):
        index_row, index_col = self.selected
        if self.cubes[index_row][index_col].value == 0:
            self.cubes[index_row][index_col].set(num_candidate)
            self.update_model()
            if is_valid_num(self.model, index_row, index_col, num_candidate) and solve_sudoku(self.model):
                return True
            else:
                self.cubes[index_row][index_col].set(0)
                self.cubes[index_row][index_col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):

        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        index_row, index_col = self.selected
        if self.cubes[index_row][index_col].value == 0:
            self.cubes[index_row][index_col].set_temp(0)

    def click(self, position):
        """
        :param: position
        :return: (index_row, index_col)
        """
        if position[0] < self.width and position[1] < self.height:
            gap = self.width / 9
            x = position[0] // gap
            y = position[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    # ==============================================================================
    # solves the sudoku board while displaying backtracking progress to GUI;
    # essentially the same as solve_sudoku(), except with additional GUI components
    def solve_gui(self):
        
        self.update_model()
        
        curr_spot = [0,0]
        find_empty_space(self.model, curr_spot)

        # validate whether we have no remaining empty spaces, meaning when we found a completed sudoku grid solution.
        if not find_empty_space(self.model, curr_spot):
            # no remaining spaces detected
            return True

        # save coordinate spots into immutable variables
        index_row = curr_spot[0]
        index_col = curr_spot[1]

        # -----------------------------------------------------
        # reaching here means there is still an empty space in sudoku grid
        # curr_spot has now been updated with an empty spot.

        # assign possible numbers to the empty curr_spot 
        for possible_num in range(1,10):

            # ONLY allow the assigning of possible_num if VALID.
            if is_valid_num(self.model, index_row, index_col, possible_num):

                # possible_num is valid; 
                # tentatively update our sudoku grid and continue solve_sudoku() for future grid cells
                self.model[index_row][index_col] = possible_num
                self.model[index_row][index_col] = possible_num
                self.cubes[index_row][index_col].set(possible_num)
                self.cubes[index_row][index_col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(20)

                if self.solve_gui():
                    # we've filled entire grid with valid numbers
                    return True
    
                # reaching here means either...
                # (1) possible_num failed validation, invalid.
                # or (2) although possible_num was valid, there was a discrepancy later on. 
                
                # undo possible_num assignment to this grid cell and try a different number
                self.model[index_row][index_col] = 0
                self.cubes[index_row][index_col].set(0)
                self.update_model()
                self.cubes[index_row][index_col].draw_change(self.win, False)
                pygame.display.update()

                # add delay so users can visually observe the backtracking
                pygame.time.delay(100)
        
        # BACKTRACKING CASE
        # reaching here means we've exhausted all possible numbers in the empty curr_spot
        # this discrepancy suggests we tentatively assigned an incorrect number somewhere previously before
        # fix this issue by undoing our most recent updates and try again
        return False

# ========================================================
# establishes a grid cell for data storage and proper GUI display
class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        update_color = ( 255, 244, 224 )
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, update_color, (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3) # green outline for tentatively updated cubes
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3) # red outline for undoing cubes w/ backtracking

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

# ========================================================
# draws to GUI; alloted time, incorrect strikes, and calls draw() matrix grid function.
def redraw_window(window, board, time, strikes): 
    
    background_color = ( 255, 238, 176 )
    window.fill(background_color)
    
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 25)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    window.blit(text, (20, 555))

    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    window.blit(text, (540 - 160, 555))
    
    # Draw grid and board
    board.draw()

# ========================================================
# prepares Time output for nice looking display
def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat

# ========================================================
# calls initial GUI functions, and listens for user inputs then passes them to functions  
def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("S U D O K U")
    board = Grid(9, 9, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    board.solve_gui()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()

# start the program
main()
# end the program
pygame.quit()

