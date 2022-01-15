
# GUI.py
import pygame
import time
from sudoku_solver import solve_sudoku, is_valid_num, find_empty_space
pygame.font.init()



# ==============================================================================

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
            pygame.time.delay(100)

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
            pygame.time.delay(100)
    
    # BACKTRACKING CASE
    # reaching here means we've exhausted all possible numbers in the empty curr_spot
    # this discrepancy suggests we tentatively assigned an incorrect number somewhere previously before
    # fix this issue by undoing our most recent updates and try again
    return False
