import copy


def add_piece_beginning(board_in, turn, position):
    """
    Add one piece at the beginning of the game

    :param board_in: Current state of the game
    :param turn: Turn of the player
    :param position: Position where the piece is going to be
    :return:
    board: New state of the game
    turn: turn of the next player
    changed: True if the board changed
    """
    board = copy.deepcopy(board_in)
    changed = False
    if is_legal_beginning(board, position, turn):
        if turn == 1:
            board[position[0]][position[1]] = 1
        else:
            board[position[0]][position[1]] = 2
        changed = True
        turn = -turn
    return [board, turn, changed]


def is_legal_beginning(state, position, turn):
    """
    Check if the new piece is in a valid position

    :param state: Current state of the game
    :param position: Position where the piece is going to be
    :param turn: Turn of the player
    :return: True if the ply is valid
    """
    if turn == 1:
        if position in validGold:
            if state[position[0]][position[1]] == 0:
                return True
    else:
        if position in validSilver:
            if state[position[0]][position[1]] == 0:
                return True
    return False


def add_piece(board_in, turns_number, turn, origin, destiny, isFlag):
    """
    Add piece to the board. Only used for human players

    :param board_in: Current state of the game
    :param turns_number: Number of turn that the player have
    :param turn: Turn of the player
    :param origin: Position of the piece
    :param destiny: New position of the piece
    :param isFlag: True if the piece is a the flag
    :return:
    board: New state of the game
    changed: True if the board changed
    is_captured: True if the move is a captured
    winner: True if the move is a winner movement
    """
    board = copy.deepcopy(board_in)
    changed = False
    is_captured = False
    winner = 0
    if is_legal(board, turns_number, origin, destiny, isFlag):
        if turn == 1:
            if board[destiny[0]][destiny[1]] == 2:
                is_captured = True
            if isFlag:
                board[destiny[0]][destiny[1]] = 3
            else:
                board[destiny[0]][destiny[1]] = 1
        else:
            if (board[destiny[0]][destiny[1]] == 1 or board[destiny[0]][destiny[1]] == 3):
                is_captured = True
            board[destiny[0]][destiny[1]] = 2
        board[origin[0]][origin[1]] = 0
        winner = check_winner(board)
        changed = True
    return [board, changed, is_captured, winner]


def check_winner(state):
    """
    Check if the current state is a the end of the game

    :param state: Current state of the game
    :return: No one win 0 | Gold wins 1 | Silver wins 2
    """
    winner = 0
    winner_positions = []
    total_gold = 0
    total_silver = 0
    is_flag = False
    for row in range(0, 11):
        for column in range(0, 11):
            if state[row][column] == 3:
                is_flag = True
                break
    if is_flag:
        for column in range(0, 11):
            winner_positions.append([0, column])
        for row in range(0, 11):
            winner_positions.append([row, 0])
        for column in range(0, 11):
            winner_positions.append([10, column])
        for row in range(0, 11):
            winner_positions.append([row, 10])
        for position in winner_positions:
            if state[position[0]][position[1]] == 3:
                winner = 1
                return winner
    else:
        winner = 2
        return winner
    for row in range(0, 11):
        for column in range(0, 11):
            if state[row][column] == 1:
                total_gold += 1
            elif state[row][column] == 2:
                total_silver += 1
    if total_silver == 0:
        return 1
    return winner


def total_pieces(state, turn):
    """
    Get the pieces of one player

    :param state: Current state of the game
    :param turn: Turn of the player
    :return: Number of pieces
    """
    total_gold = 0
    total_silver = 0
    for row in range(0, 11):
        for column in range(0, 11):
            if state[row][column] == 1:
                total_gold += 1
            elif state[row][column] == 2:
                total_silver += 1
    if turn == 1:
        return total_gold
    else:
        return total_silver


def in_range(position):
    """
    Check if the position is in the range of the board

    :param position: Position to check
    :return: True if it is a valid position
    """
    if (position[0] < 0 or position[0] > 10 or position[1] < 0 or position[1] > 10):
        return False
    return True


def is_legal(state, turns_number, origin, destiny, isFlag):
    """
    Check if the move is legal

    :param state: Current state of the game
    :param turns_number: Number of turn that the player have
    :param origin: Position of the piece
    :param destiny: New position of the piece
    :param isFlag: True if the piece is a the flag
    :return: True if the move is legal
    """
    movements = possible_movements(state, turns_number, origin, isFlag)
    for movement in movements:
        if destiny == movement:
            return True
    return False


def possible_movements(state, turns_number, position, isFlag):
    """
    Get the possible movements from one position

    :param state: Current state of the game
    :param turns_number: Number of turn that the player have
    :param position: Position to obtain the movements
    :param isFlag: True if the piece is a the flag
    :return: List of the possible movements
    """
    row = position[0]
    column = position[1]
    piece = state[row][column]
    turn = 0
    if (piece == 1 or piece == 3):
        turn = 1
    movements = []
    if turns_number == 2:
        if turn == 1:
            if (in_range([row-1, column-1]) and state[row-1][column-1] == 2):
                movements.append([row-1, column-1])
            if (in_range([row-1, column+1]) and state[row-1][column+1] == 2):
                movements.append([row-1, column+1])
            if (in_range([row+1, column-1]) and state[row+1][column-1] == 2):
                movements.append([row+1, column-1])
            if (in_range([row+1, column+1]) and state[row+1][column+1] == 2):
                movements.append([row+1, column+1])
        else:
            if (in_range([row-1, column-1]) and state[row-1][column-1] == 1):
                movements.append([row-1, column-1])
            if (in_range([row-1, column+1]) and state[row-1][column+1] == 1):
                movements.append([row-1, column+1])
            if (in_range([row+1, column-1]) and state[row+1][column-1] == 1):
                movements.append([row+1, column-1])
            if (in_range([row+1, column+1]) and state[row+1][column+1] == 1):
                movements.append([row+1, column+1])
            if (in_range([row-1, column-1]) and state[row-1][column-1] == 3):
                movements.append([row-1, column-1])
            if (in_range([row-1, column+1]) and state[row-1][column+1] == 3):
                movements.append([row-1, column+1])
            if (in_range([row+1, column-1]) and state[row+1][column-1] == 3):
                movements.append([row+1, column-1])
            if (in_range([row+1, column+1]) and state[row+1][column+1] == 3):
                movements.append([row+1, column+1])
        for x in range(row, -1, -1):
            if x != row:
                if state[x][column] == 0:
                    movements.append([x, column])
                else:
                    break
        for x in range(row, 11):
            if x != row:
                if state[x][column] == 0:
                    movements.append([x, column])
                else:
                    break
        for y in range(column, -1, -1):
            if y != column:
                if state[row][y] == 0:
                    movements.append([row, y])
                else:
                    break
        for y in range(column, 11):
            if y != column:
                if state[row][y] == 0:
                    movements.append([row, y])
                else:
                    break
    elif not isFlag:
        for x in range(row, -1, -1):
            if x != row:
                if state[x][column] == 0:
                    movements.append([x, column])
                else:
                    break
        for x in range(row, 11):
            if x != row:
                if state[x][column] == 0:
                    movements.append([x, column])
                else:
                    break
        for y in range(column, -1, -1):
            if y != column:
                if state[row][y] == 0:
                    movements.append([row, y])
                else:
                    break
        for y in range(column, 11):
            if y != column:
                if state[row][y] == 0:
                    movements.append([row, y])
                else:
                    break
    return movements


def get_enemy_pieces(state, enemy):
    total_enemy_pieces = 0
    for x in range(0, 11):
        for y in range(0, 11):
            if state[x][y] == enemy:
                total_enemy_pieces = total_enemy_pieces + 1
    return total_enemy_pieces


def go_near_flag(state, player):
    flag_position = get_flag_position(state)
    turn = -1
    row = flag_position[0]
    column = flag_position[1]
    if player == 1:
        turn = 1
    number_enemies = 0
    if turn == 1:
        if (in_range([row - 1, column - 1]) and state[row - 1][column - 1] == 2):
            number_enemies += 1
        if (in_range([row - 1, column + 1]) and state[row - 1][column + 1] == 2):
            number_enemies += 1
        if (in_range([row + 1, column - 1]) and state[row + 1][column - 1] == 2):
            number_enemies += 1
        if (in_range([row + 1, column + 1]) and state[row + 1][column + 1] == 2):
            number_enemies += 1
    return number_enemies


def future_captures(state, player):
    """
    Get the number of possible captures in the board
    TODO: check if it is actually working
    :param state: Current state of the game
    :param player: Player to analyze
    :return: Number of captures
    """
    count = 0
    for x in range(0, 11):
        for y in range(0, 11):
            if state[x][y] == player:
                count = count + check_enemies_around(state, [x, y], player)
    return count


def block_flag(state, player):
    """
    Check if the flag in the board is blocked
    TODO: check if it is actually working
    :param state: Current state of the game
    :param player: Player to analyze
    :return: number of blocks of the flag, max = 4 (up, down, right, left)
    """
    number_blocks = 0

    if player == 2:
        flag_position = get_flag_position(state)
        if flag_position != []:
            [up, down, left, right] = flag_to_board_border(flag_position)
            for position in up:
                if position != 0:
                    number_blocks = number_blocks + 1
                    break
            for position in down:
                if position != 0:
                    number_blocks = number_blocks + 1
                    break
            for position in left:
                if position != 0:
                    number_blocks = number_blocks + 1
                    break
            for position in right:
                if position != 0:
                    number_blocks = number_blocks + 1
                    break
    return number_blocks


def check_enemies_around(state, position, player):
    """
    Check if a piece has enemies that can be captured

    :param state: Current state of the game
    :param position: Position to obtain the movements
    :param player: Player to analyze
    :return: number of enemies around the piece in the position
    """
    turn = -1
    row = position[0]
    column = position[1]
    if player == 1:
        turn = 1
    number_enemies = 0
    if turn == 1:
        if (in_range([row - 1, column - 1]) and state[row - 1][column - 1] == 2):
            number_enemies += 1
        if (in_range([row - 1, column + 1]) and state[row - 1][column + 1] == 2):
            number_enemies += 1
        if (in_range([row + 1, column - 1]) and state[row + 1][column - 1] == 2):
            number_enemies += 1
        if (in_range([row + 1, column + 1]) and state[row + 1][column + 1] == 2):
            number_enemies += 1
    else:
        if (in_range([row - 1, column - 1]) and state[row - 1][column - 1] == 1):
            number_enemies += 1
        if (in_range([row - 1, column + 1]) and state[row - 1][column + 1] == 1):
            number_enemies += 1
        if (in_range([row + 1, column - 1]) and state[row + 1][column - 1] == 1):
            number_enemies += 1
        if (in_range([row + 1, column + 1]) and state[row + 1][column + 1] == 1):
            number_enemies += 1
        if (in_range([row - 1, column - 1]) and state[row - 1][column - 1] == 3):
            number_enemies += 1
        if (in_range([row - 1, column + 1]) and state[row - 1][column + 1] == 3):
            number_enemies += 1
        if (in_range([row + 1, column - 1]) and state[row + 1][column - 1] == 3):
            number_enemies += 1
        if (in_range([row + 1, column + 1]) and state[row + 1][column + 1] == 3):
            number_enemies += 1
    return number_enemies


def get_flag_position(board):
    """
    Get the position of the flag in the board

    :param board: Current state of the game
    :return: The position of the flag
    """
    flag_position = []
    for row in range(0, 11):
        for column in range(0, 11):
            if board[row][column] == 3:
                flag_position = [row, column]
                return flag_position
    return flag_position


def flag_to_board_border(flag_position):
    """
    Get positions from the flag position to the border of the board

    :param flag_position: Position of the flag
    :return: Lists of the four directions
    up: List from the flag position to the top of the board
    down: List from the flag position to the bottom of the board
    left: List from the flag position to the left of the board
    right: List from the flag position to the right of the board
    """
    up, down, left, right = [], [], [], []
    row = flag_position[0]
    column = flag_position[1]
    for x in range(row, -1, -1):
        left.append([x, column])
    for x in range(row, 11):
        right.append([x, column])
    for y in range(column, -1, -1):
        up.append([row, y])
    for y in range(column, 11):
        left.append([row, y])
    return [up, down, left, right]


validGold = []
validSilver = []

for x in range(0, 11):
    for y in range(0, 11):
        if 3 <= x <= 7:
            if 3 <= y <= 7:
                validGold.append([x, y])
            else:
                validSilver.append([x, y])
        else:
            validSilver.append([x, y])