def solve_n_queens(n):
    def is_safe(board, row, col):
        for i in range(row):
            if board[i] == col or \
               board[i] - i == col - row or \
               board[i] + i == col + row:
                return False
        return True

    def solve(row):
        if row == n:
            result.append(board[:])
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                solve(row + 1)
    result =[]
    board= [-1]*n
    solve(0)
    for sol in result:
        for i in sol:
            print("."* i +"q" +"." *(n - i - 1))
        print("\n")
n = 8
solve_n_queens(n)
