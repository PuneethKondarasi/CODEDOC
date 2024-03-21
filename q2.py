board = eval(input())
def countBattleships(board):
    if not board:
        return 0

    count = 0
    rows, cols = len(board), len(board[0])

    for i in range(rows):
        for j in range(cols):
            if board[i][j] == 'X':
                if i > 0 and board[i-1][j] == 'X':
                    continue
                if j > 0 and board[i][j-1] == 'X':
                    continue
                count += 1
    return count
print(countBattleships(board))
