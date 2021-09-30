import random
from copy import deepcopy
from math import exp

# global variables
board_size = 0


# print board matrix-wise
def print_board(board):
    for i in range(board_size):
        for j in range(board_size):
            print(board[i][j], end=' ')
        print()


# randomly place (n - 1) queens on the board
def place_queens(board):
    count = 0

    while count < board_size:
        row = random.randint(0, board_size - 1)
        col = count  # a unique column for every queen

        board[row][col] = 1
        count += 1


# returns list of queen indexes (each index is tuple of (x, y)
def get_queens(board):
    pos = []
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == 1:
                tup = i, j
                pos.append(tup)

    return pos


# objective function (calculates heuristic)
def attacking_queens(board):
    positions = get_queens(board)
    attacking = 0

    # for every queen
    for i in range(len(positions)):
        queen_pos = positions[i]

        # check all other queens
        for j in range(len(positions)):

            # don't compare queen with itself
            if i != j:

                # get position of other queen
                other_pos = positions[j]

                # same row check (columns are already unique)
                if other_pos[0] == queen_pos[0]:
                    attacking += 1

                ############## checking for diagonals ##################

                other_x, other_y = other_pos[0], other_pos[1]

                # northwest diagonal (decrement row and column)

                x = deepcopy(queen_pos[0])
                y = deepcopy(queen_pos[1])

                while x >= 0 and y >= 0:
                    x -= 1
                    y -= 1

                    # is the other queen present at this possible x, y ?
                    if x == other_x and y == other_y:
                        attacking += 1

                # southeast diagonal (increment row and column_

                x = deepcopy(queen_pos[0])
                y = deepcopy(queen_pos[1])

                while x < board_size and y < board_size:
                    x += 1
                    y += 1

                    # is the other queen present at this possible x, y ?
                    if x == other_x and y == other_y:
                        attacking += 1

                # southwest diagonal (increment row, decrement column)

                x = deepcopy(queen_pos[0])
                y = deepcopy(queen_pos[1])

                while x < board_size and y >= 0:
                    x += 1
                    y -= 1

                    # is the other queen present at this possible x, y ?
                    if x == other_x and y == other_y:
                        attacking += 1

                # northeast diagonal (decrement row, increment column)

                x = deepcopy(queen_pos[0])
                y = deepcopy(queen_pos[1])

                while x >= 0 and y < board_size:
                    x -= 1
                    y += 1

                    # is the other queen present at this possible x, y ?
                    if x == other_x and y == other_y:
                        attacking += 1

    return int(attacking / 2)


# get list of possible next boards
def expand_board(board, positions):
    boards = []

    # for every queen
    for i in range(len(positions)):

        # get queen index
        x = deepcopy(positions[i][0])
        y = deepcopy(positions[i][1])

        # move queen up and down to other rows (same column)
        for j in range(board_size):

            # no need to move to the column it is already in
            if x != j:
                b = deepcopy(board)

                # swap values and move queen
                b[x][y] = 0
                b[j][y] = 1

                # add this board to list of boards
                boards.append(b)

    return boards


# gets all immediate neighbours of all queens
def get_neighbours(board):
    neighbours = []
    positions = get_queens(board)

    for pos in positions:
        x = pos[0]
        y = pos[1]

        if x > 0:
            b = deepcopy(board)
            b[x][y] = 0
            b[x - 1][y] = 1
            neighbours.append(b)

        if x < board_size - 1:
            b = deepcopy(board)
            b[x][y] = 0
            b[x + 1][y] = 1
            neighbours.append(b)

    return neighbours


# make one queen move randomly
def move_random_queen(board):
    random_col = random.randint(0, len(board) - 1)
    random_row = random.randint(0, len(board) - 1)

    for row, col in get_queens(board):
        if col == random_col:
            while row == random_row:
                random_row = random.randint(0, len(board) - 1)

            b = deepcopy(board)
            b[random_row][col], b[row][col] = b[row][col], b[random_row][col]
            return b


# sort boards list and return board with least # of attacking queens
def get_min_board(boards):
    boards.sort(key=attacking_queens)
    return boards[0]


# actual algorithm (steepest ascent hill climbing)
def hill_climbing(board):
    moves = 0

    while True:
        moves += 1

        # obtain queen indexes and heuristic of current board
        positions = get_queens(board)
        h = attacking_queens(board)

        # get all possible next moves of this  board
        boards = expand_board(board, positions)

        # get board with minimum h
        min_board = get_min_board(boards)
        min_h = attacking_queens(min_board)

        # if no next moves are better than current
        if min_h >= h:
            return board, moves, h

        # solution found
        elif min_h == 0:
            return min_board, moves, min_h

        else:
            board = min_board


# algorithm simulated annealing
def simulated_annealing(board, max_t):
    curr = board
    moves = 0

    for t in range(1, max_t):

        if t % 1000 == 0:
            print("Simulated Annealing in progress... ( iteration #", t, ')')

        T = ((t + 1) / max_t)
        moves += 1

        # obtain queen indexes and heuristic of current board
        curr_h = attacking_queens(curr)

        # choose a random number
        neighbour = move_random_queen(curr)
        neighbour_h = attacking_queens(neighbour)

        delta = neighbour_h - curr_h
        e = (-delta) / T

        if e < 0:
            curr = neighbour

        try:
            if random.uniform(0, 1) < exp(e):
                curr = neighbour
        except:
            pass

        if neighbour_h == 0:
            return neighbour, moves

    return curr, moves


def main():
    global board_size
    board_size = int(input("Enter number of queens: "))

    board = []

    for i in range(board_size):
        row = []
        for j in range(board_size):
            row.append(0)

        board.append(row)

    # board = [
    #     [0, 0, 0, 0, 0, 0, 0, 0],  # 0
    #     [0, 0, 0, 0, 0, 0, 0, 0],  # 1
    #     [0, 0, 0, 0, 0, 0, 0, 0],  # 2
    #     [0, 0, 0, 0, 0, 0, 0, 0],  # 3
    #     [0, 0, 0, 0, 0, 0, 0, 0],  # 4
    #     [0, 0, 0, 0, 0, 0, 0, 0],  # 5
    #     [0, 0, 0, 0, 0, 0, 0, 0],  # 6
    #     [0, 0, 0, 0, 0, 0, 0, 0],  # 7
    # ]

    print("\n-------------------------------")
    print("Initial board:\n")

    place_queens(board)
    print_board(board)

    print("\n------------- Hill Climbing ------------------")
    result, moves, h = hill_climbing(board)

    print("\nThe best board found is:\n")
    print_board(result)

    print("\nNo of attacking queens: ", h)
    print("Total number of moves: ", moves)

    print("\n------------- Simulated Annealing ------------------\n")
    max_t = 100000
    result, moves = simulated_annealing(board, max_t)

    print("\nThe best board found is:\n")
    print_board(result)

    print("\nNo of attacking queens: ", attacking_queens(result))
    print("Total number of moves: ", moves)


if __name__ == "__main__":
    main()
