
# ==============================================
# identifies whether there exists an empty spot within the given array
def find_empty_space(arr, empty_spot):
    for index_row in range(len(arr)):
        for index_col in range(len(arr[0])):
            if arr[index_row][index_col] == 0:
                empty_spot[0] = index_row
                empty_spot[1] = index_col
                return True
    return False

# ==============================================
# validates whether the given integer exists within the given row of matrix grid


# ==============================================
# validates whether the given integer exists within the given column of matrix grid


# ==============================================
# validates whether the given integer exists within the corresponding 3x3 quadrant of matrix grid



# ==============================================
# primary sudoku solver function that uses the backtracking algorithm to input, validate, tweak, and eventually solve sudoku!

def solve_sudoku(arr):
    spot = [0,0]
    print(find_empty_space(my_arr, spot))
    print(spot)

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

