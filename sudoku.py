
# ==============================================
# identifies whether there exists an empty spot within the given array.
def find_empty_space(arr, empty_spot):
    for index_row in range(len(arr)):
        for index_col in range(len(arr[0])):
            if arr[index_row][index_col] == 0:
                empty_spot[0] = index_row
                empty_spot[1] = index_col
                return True
    return False

# ==============================================
# validates whether the given integer isn't within the given row of matrix grid.
def valid_in_row(arr, index_row, num_candidate):
    if num_candidate not in arr[index_row]:
        return True
    else:
        return False

# ==============================================
# validates whether the given integer exists within the given column of matrix grid.
def valid_in_col(arr, index_col, num_candidate):
    for index_row in range(len(arr)):
        if arr[index_row][index_col] == num_candidate:
            return False
    return True

# ==============================================
# validates whether the given integer exists within the corresponding 3x3 quadrant of matrix grid.
def valid_in_quadrant(arr, index_row, index_col, num_candidate):
    # obtain desired quadrant rows
    if index_row < 3:
        rows = arr[:3]
    elif index_row < 6:
        rows = arr[3:6]
    else:
        rows = arr[6:]
    # obtain desired quadrant columns
    if index_col < 3:
        for row in rows:
            for i in range(0,3):
                if row[i] == num_candidate:
                    return False
        return True
    elif index_col < 6:
        for row in rows:
            for i in range(0,6):
                if row[i] == num_candidate:
                    return False
        return True
    else:
        for row in rows:
            for i in range(0,9):
                if row[i] == num_candidate:
                    return False
        return True

# ==============================================
# num_candidate must be unique to row, unique to column, and unique to 3x3 grid quadrant
def is_valid_num(arr, index_row, index_col, num_candidate):
    if valid_in_row(arr, index_row, num_candidate) and valid_in_col(arr, index_col, num_candidate) and valid_in_quadrant(arr, index_row, index_col, num_candidate):
        return True
    else:
        return False

# ==============================================
# primary sudoku solver function that uses the backtracking algorithm to input, validate, tweak, and eventually solve sudoku!

def solve_sudoku(arr):

    # -----------------------------------------------------

    # keep track of empty coordinate spots
    # update curr_spot using find_empty_space() function.
    curr_spot = [0,0] 

    # validate whether we have no remaining empty spaces, meaning when we found a completed sudoku grid solution.
    if not find_empty_space(arr, curr_spot):
        # no remaining spaces detected
        print(arr)
        return True
    
    # save coordinate spots into immutable variables
    index_row = curr_spot[0]
    index_col = curr_spot[1]
    print('SOLVE SUDOKU, FOUND EMPTY SPOT:', index_row, index_col, arr[0])
    # -----------------------------------------------------
    # reaching here means there is still an empty space in sudoku grid
    # curr_spot has now been updated with an empty spot.

    # assign possible numbers to the empty curr_spot 
    for possible_num in range(1,10):

        # ONLY allow the assigning of possible_num if VALID.
        print('SOLVE SUDOKU, FOUND EMPTY SPOT:', index_row, index_col, possible_num, arr[0])
        if is_valid_num(arr, index_row, index_col, possible_num):
            print(index_row, index_col, possible_num)
            # possible_num is valid; 
            # tentatively update our sudoku grid and continue solve_sudoku() for future grid cells
            arr[index_row][index_col] = possible_num
            print(arr)
            if solve_sudoku(arr):
                print('HELLO')
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

my_arr = [[3, 1, 6, 5, 0, 8, 4, 0, 0],
          [5, 2, 0, 0, 0, 0, 0, 0, 0],
          [0, 8, 7, 0, 0, 0, 0, 3, 1],
          [0, 0, 3, 0, 1, 0, 0, 8, 0],
          [9, 0, 0, 8, 6, 3, 0, 0, 5],
          [0, 5, 0, 0, 9, 0, 6, 0, 0],
          [1, 3, 0, 0, 0, 0, 2, 5, 0],
          [0, 0, 0, 0, 0, 0, 0, 7, 4],
          [0, 0, 5, 2, 0, 6, 3, 0, 0]]

solve_sudoku(my_arr)
#print(my_arr)
test =   [[3, 1, 6, 5, 0, 8, 4, 0, 0],
          [5, 2, 0, 0, 0, 0, 0, 0, 0],
          [0, 8, 7, 0, 0, 0, 0, 3, 1],
          [0, 0, 3, 0, 1, 0, 0, 8, 0],
          [9, 0, 0, 8, 6, 3, 0, 0, 5],
          [0, 5, 0, 0, 9, 0, 6, 0, 0],
          [1, 3, 0, 0, 0, 0, 2, 5, 0],
          [0, 0, 0, 0, 0, 0, 0, 7, 4],
          [0, 0, 5, 2, 0, 6, 3, 0, 0]]
print(valid_in_row(test, 0, 7))
print(valid_in_col(test, 4, 7))
print(valid_in_quadrant(test, 0, 4, 7))