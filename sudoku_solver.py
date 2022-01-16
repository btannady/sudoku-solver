"""
sudoku_solver.py

contains functions necessary for auto-solving sudoku
"""


# ==============================================
# displays solved sudoku board nicely to the console
def display_grid(arr):

    for index_row in range(len(arr)):
        if index_row in (3,6,9):
            print('======================')
        
        for index_col in range(len(arr[0])):
            if index_col in (3,6,9):
                print('|', end=" ")
            print(arr[index_row][index_col], end=" ")
        print(end="\n")

# ==============================================
# validates whether there exists an empty spot within the given array, if so then sets empty_spot to those coordinates.
def find_empty_space(arr, empty_spot):
    for index_row in range(len(arr)):
        for index_col in range(len(arr[0])):
            if arr[index_row][index_col] == 0:
                empty_spot[0] = index_row
                empty_spot[1] = index_col
                return True
    return False

# ==============================================
# validates whether the given integer isn't within any other cell in the given row of matrix grid.
def valid_in_row(arr, index_row, index_col, num_candidate):
    for curr_col in range(len(arr[index_row])):
        if arr[index_row][curr_col] == num_candidate and curr_col != index_col:
            return False
    return True

# ==============================================
# validates whether the given integer exists within any other cell in the given column of matrix grid.
def valid_in_col(arr, index_row, index_col, num_candidate):
    for curr_row in range(len(arr)):
        if arr[curr_row][index_col] == num_candidate and curr_row != index_row:
            return False
    return True

# ==============================================
# validates whether the given integer exists within any other cell in the corresponding 3x3 quadrant of matrix grid.
def valid_in_quadrant(arr, index_row, index_col, num_candidate):
    # obtain desired quadrant rows
    if index_row < 3:
        rows = (0, 1, 2)
    elif index_row < 6:
        rows = (3, 4, 5)
    else:
        rows = (6, 7, 8)
  
    # obtain desired quadrant columns
    if index_col < 3:
        for curr_row in rows:
            for curr_col in range(0,3):
                if arr[curr_row][curr_col] == num_candidate and (curr_row, curr_col) != (index_row, index_col):
                    return False
        return True
    elif index_col < 6:
        for curr_row in rows:
            for curr_col in range(3,6):
                if arr[curr_row][curr_col] == num_candidate and (curr_row, curr_col) != (index_row, index_col):
                    return False
        return True
    else:
        for curr_row in rows:
            for curr_col in range(6,9):
                if arr[curr_row][curr_col] == num_candidate and (curr_row, curr_col) != (index_row, index_col):
                    return False
        return True

# ==============================================
# num_candidate must be unique to row, unique to column, and unique to 3x3 grid quadrant
def is_valid_num(arr, index_row, index_col, num_candidate):
    if valid_in_row(arr, index_row, index_col, num_candidate) and valid_in_col(arr, index_row, index_col, num_candidate) and valid_in_quadrant(arr, index_row, index_col, num_candidate):
        return True
    else:
        return False

# ==============================================
# primary sudoku solver function that uses the backtracking algorithm to input, validate, tweak, and eventually solve sudoku!

def solve_sudoku(arr):

    # keep track of empty coordinate spots
    # update curr_spot using find_empty_space() function.
    curr_spot = [0,0] 

    # validate whether we have no remaining empty spaces, meaning when we found a completed sudoku grid solution.
    if not find_empty_space(arr, curr_spot):
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
        if is_valid_num(arr, index_row, index_col, possible_num):

            # possible_num is valid; 
            # tentatively update our sudoku grid and continue solve_sudoku() for future grid cells
            arr[index_row][index_col] = possible_num
            
            if solve_sudoku(arr):
                # we've filled entire grid with valid numbers
                return True
 
            # reaching here means either...
            # (1) possible_num failed validation, invalid.
            # or (2) although possible_num was valid, there was a discrepancy later on. 
            
            # undo possible_num assignment to this grid cell and try a different number
            arr[index_row][index_col] = 0
    
    # BACKTRACKING CASE
    # reaching here means we've exhausted all possible numbers in the empty curr_spot
    # this discrepancy suggests we tentatively assigned an incorrect number somewhere previously before
    # fix this issue by undoing our most recent updates and try again
    return False

    # -----------------------------------------------------

# ==============================================

'''
# Example Sudodu Grid (unsolved)
my_arr =[
        [0, 6, 0, 3, 0, 0, 8, 0, 4],
        [5, 3, 7, 0, 9, 0, 0, 0, 0], 
        [0, 4, 0, 0, 0, 6, 3, 0, 7],
        [0, 9, 0, 0, 5, 1, 2, 3, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [7, 1, 3, 6, 2, 0, 0, 4, 0],
        [3, 0, 6, 4, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 6, 0, 5, 2, 3],
        [1, 0, 2, 0, 0, 9, 0, 8, 0]]
          
# Display Sudoku Grid (unsolved)
print('< UNSOLVED SUDOKU GRID >')
display_grid(my_arr)

# Begin Program !
solve_sudoku(my_arr)
print()

# Display Sudoku Grid (solved)
print('< SOLVED SUDOKU GRID >')
display_grid(my_arr)

'''
