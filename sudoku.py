
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
# simply calls the three validation checks for whether it's okay to input a number candidate in an empty cell.
def is_valid_num(arr, index_row, index_col, num_candidate):
    if valid_in_row(arr, index_row, num_candidate) and valid_in_col(arr, index_col, num_candidate) and valid_in_quadrant(arr, index_row, index_col, num_candidate):
        return True
    else:
        return False

# ==============================================
# primary sudoku solver function that uses the backtracking algorithm to input, validate, tweak, and eventually solve sudoku!

def solve_sudoku(arr):
    spot = [0,0]
    print(find_empty_space(my_arr, spot))
    print(spot)
    for i in range(1,10):
        if is_valid_num(arr, spot[0], spot[1], i):
            print(True, i)
        else:
            print(False, i)


# ==============================================

my_arr = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
          [5, 2, 0, 0, 0, 0, 0, 0, 0],
          [0, 8, 7, 0, 0, 0, 0, 3, 1],
          [0, 0, 3, 0, 1, 0, 0, 8, 0],
          [9, 0, 0, 8, 6, 3, 0, 0, 5],
          [0, 5, 0, 0, 9, 0, 6, 0, 0],
          [1, 3, 0, 0, 0, 0, 2, 5, 0],
          [0, 0, 0, 0, 0, 0, 0, 7, 4],
          [0, 0, 5, 2, 0, 6, 3, 0, 0]]

solve_sudoku(my_arr)

