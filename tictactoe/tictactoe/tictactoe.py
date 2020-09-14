"""
Tic Tac Toe Player
"""

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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # https://stackoverflow.com/questions/43082149/simple-way-to-count-number-of-specific-elements-in-2d-array-python
    x_count = sum([row.count(X) for row in board])
    o_count = sum([row.count(O) for row in board])
    return O if o_count < x_count else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Iterate through all rows and columns adding an action for open spaces.
    actions = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            # Anytime a cell is open, that makes it a possible action.
            if board[i][j] is EMPTY:
                actions.append((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Make a deep copy of the current board
    # https://stackoverflow.com/questions/6532881/how-to-make-a-copy-of-a-2d-array-in-python
    # https://stackoverflow.com/questions/36968157/what-is-the-fastest-way-to-copy-a-2d-array-in-python
    board_copy = [row[:] for row in board]

    # Assign the space as the current player's symbol
    if board_copy[action[0]][action[1]] is EMPTY:
        board_copy[action[0]][action[1]] = player(board_copy)
    else:
        # If the action argument was invalid, raise an exception.
        raise ValueError("action is not valid for board")

    # Return the copied board with the new action in place.
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Create a dictionary to assign values for each possible key.
    # These keys will be used to sum up the value across rows, columns, and diagonals.
    cell_values = {
        "X": 1,
        "O": -1,
        None: 0
    }

    # Check for diagonal, row-wise, and column-wise terminal conditions
    down_right_diagonal_value = 0
    down_left_diagonal_value = 0
    for i in range(len(board)):

        # These are the diagonal win condition checks
        # Anytime a diagonal's sum is 3 or -3 then it is a win condition.
        down_right_diagonal_value += cell_values[board[i][i]]
        down_left_diagonal_value += cell_values[board[i][len(board) - 1 - i]]
        if down_right_diagonal_value is 3 or down_left_diagonal_value is 3:
            return X
        elif down_right_diagonal_value is -3 or down_left_diagonal_value is -3:
            return O

        # These are the column and row win condition checks
        # Anytime a row or column's sum is 3 or -3 then it is a win condition.
        row_value = 0
        column_value = 0
        for j in range(len(board[i])):
            row_value += cell_values[board[i][j]]
            column_value += cell_values[board[j][i]]
        if row_value is 3 or column_value is 3:
            return X
        elif row_value is -3 or column_value is -3:
            return O

    # Return None if no X or O win conditions were found
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If there is a winner, than the game is over.
    if winner(board) is not None:
        return True
    else:
        # Check if the board has any empty spaces
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] is EMPTY:
                    # Stop as soon as an empty cell is found.
                    # With no winner and an empty cell, the game is not over.
                    # (short-circuit removes need to call actions(board) here)
                    return False

    # Return true since there are no moves remaining
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # https://stackoverflow.com/questions/44636514/python-multiple-nested-ternary-expression
    return 1 if winner(board) is X else -1 if winner(board) is O else 0


def get_best_move(board):
    """
    Returns the best move (value, action) pair for current board and player using Minimax.
    """
    # Return the utility of the current board if this is a terminal state.
    if terminal(board):
        # The action is None because no further actions can be taken.
        return (utility(board), None)
    
    # Determine which player's move it is
    current_player = player(board)

    # Set the starting value below all possible action values
    best_move = (-2 if current_player is X else 2, None)

    # Check every action to determine the best one
    for action in actions(board):
        # Recursively get the best move for this action.
        action_result = get_best_move(result(board, action))
        
        # See if this action is better than a previous one.
        # If it is better, store it.
        if ((current_player is X and action_result[0] > best_move[0]) or
                (current_player is O and action_result[0] < best_move[0])):
            best_move = (action_result[0], action)

    # Return the best available move.
    # If multiple moves are equally good, this returns the first.
    return best_move


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Return None since no further moves can be made in a terminal state.
    if terminal(board):
        return None
    
    # Use a recursive Minimax function to return the best available move.
    return get_best_move(board)[1]
