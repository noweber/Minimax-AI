"""
Tic Tac Toe Player
"""

from copy import deepcopy #TODO should I use result_board = [row[:] for row in board] instead?
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

# TODO
def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
          if(cell is X):
            x_count += 1
          elif(cell is O):
            o_count += 1
    return O if o_count < x_count else X

# TODO
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is EMPTY:
                actions.append((i, j))
    return actions

# TODO
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # TODO: raise ValueError("action is not valid for board")
    result_board = deepcopy(board)
    if result_board[action[0]][action[1]] is EMPTY:
        result_board[action[0]][action[1]] = player(result_board)
    return result_board

# TODO
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # loser = player(board)
    # if loser is X:
    #     return O
    # elif :
    #     return X
    
    cell_values = {
        "X": 1,
        "O": -1,
        None: 0
    }

    # Check for row-wise terminal conditions
    for i in range(len(board)):
        row_value = 0
        for j in range(len(board[i])):
            row_value += cell_values[board[i][j]]
        if row_value is 3:
            return X
        elif row_value is -3:
            return O

    # Check for column-wise terminal conditions
    # Note that this assumes the number of columns equals the number of rows.
    for i in range(len(board)):
        column_value = 0
        for j in range(len(board[i])):
            column_value += cell_values[board[j][i]]
        if column_value is 3:
            return X
        elif column_value is -3:
            return O

    # Check for down-right diagnoal win condition
    diagonal_value = 0
    for i in range(len(board)):
        diagonal_value += cell_values[board[i][i]]
        if diagonal_value is 3:
            return X
        elif diagonal_value is -3:
            return O

    # Check for down-left diagnoal win condition
    diagonal_value = 0
    for i in range(len(board)):
        diagonal_value += cell_values[board[i][len(board) - 1 - i]]
        if diagonal_value is 3:
            return X
        elif diagonal_value is -3:
            return O

    # Return None if no X or O win conditions were found
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    winning_player = winner(board)
    if winning_player is not None:
        return True
    else:
        # Check if the board has any possible remaining moves (any empty spaces)
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] is EMPTY:
                    return False

    # Return true since there is no winner and there are no empty spaces remaining
    return True

# TODO
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winning_player = winner(board)
    if winning_player is X:
        return 1
    elif winning_player is O:
        return -1
    else:
        return 0

def max_value(board):
    if terminal(board):
        return utility(board)
    
    # Set the starting value below all possible action values
    value = -2

    for action in actions(board):
        value = max(value, min_value(result(board, action)))

    return value

def min_value(board):
    if terminal(board):
        return utility(board)
    
    # Set the starting value below all possible action values
    value = 2

    for action in actions(board):
        value = min(value, max_value(result(board, action)))

    return value

# TODO
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # TODO: if the board is terminal, return none
    if terminal(board):
        return None
    
    best_action = None
    if player(board) is X:
        best_value = -2
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_value:
                best_action = action
                best_value = value
    else:
        best_value = 2
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_value:
                best_action = action
                best_value = value
    
    return best_action
