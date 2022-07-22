from RulesAction import *
import random
import copy

INF = 99999999999999
MAX_SCORE = 1000
ENEMIES_AROUND = 20
BLOCK_FLAG = 10
BLAG_ESCAPE = 10

def make_move(state, turn, t_table, hashtable):
    """
    Create a move for the AI

    :param state: Current state of the game
    :param turn: The turn of the player -1 (silver) | 1 (gold)
    :param t_table: Transposition table of the player
    :param hashtable: The hashtable of the game
    :return: [state, turn, False, winner]
    state = New state after the movement
    turn = Turn of the next player
    changed = True if the state
    """
    board = copy.deepcopy(state)
    move = [-1, -1]
    score = -INF
    if turn == 1:
        player = 1
    else:
        player = 2
    gold_pieces = get_enemy_pieces(state, 1)
    silver_pieces = get_enemy_pieces(state, 2)
    moves = generate_moves(state, 2, turn)
    for m in moves:
        if len(m) == 2:
            [board, aux_turn, winner, changed] = add_piece_to_table(state, turn, m[0], m[1])
        else:
            [board, aux_turn, winner, changed] = add_two_pieces(state, turn, m)
        temp = minmax(state, gold_pieces, silver_pieces, player, 2, turn, 1)
        # temp = -alphabeta_negamax(state, gold_pieces, silver_pieces, player, 2, turn, 2, -INF, +INF)
        # temp = -alphabeta_nega_transposition_table(state, gold_pieces, silver_pieces, player, 2, turn, 2, -INF, +INF, t_table, hashtable)
        # temp = -pvs(state, gold_pieces, silver_pieces,  player, 2, turn, 2, -INF, +INF)
        if temp >= (MAX_SCORE - 10):
            move = m
            break;
        if temp >= score:
            score = temp
            move = m
    if len(move) == 2:
        [state, turn, winner, changed] = add_piece_to_table(state, turn, move[0], move[1])
    else:
        [state, turn, winner, changed] = add_two_pieces(state, turn, move)
    # turn = -turn
    print("AI move: ", move, get_enemy_pieces(state, 1), get_enemy_pieces(state, 2))
    return [state, turn, False, winner]


def add_two_pieces(state, turn, moves):
    """
    Make two moves in the board

    :param state: Current state of the game
    :param turn: The turn of the player -1 (silver) | 1 (gold)
    :param moves: List of moves that we have to make.
    :return: [board, turn, winner, changed]
    board = New state after the movement
    turn = Turn of the next player
    winner = No one win 0 | Gold wins 1 | Silver wins 2
    changed = True if the state
    """
    board = copy.deepcopy(state)
    board[moves[0][0]][moves[0][1]] = 0
    board[moves[2][0]][moves[2][1]] = 0
    if turn == 1:
        board[moves[1][0]][moves[1][1]] = 1
        board[moves[3][0]][moves[3][1]] = 1
    else:
        board[moves[1][0]][moves[1][1]] = 2
        board[moves[3][0]][moves[3][1]] = 2
    winner = check_winner(board)
    changed = True
    turn = -turn
    return [board, turn, winner, changed]


def add_piece_to_table(state, turn, origin, position):
    """
    Make one move in the board

    :param state: Current state of the game
    :param turn: The turn of the player -1 (silver) | 1 (gold)
    :param origin: Position of the piece
    :param position: New position of the piece
    :return: [board, turn, winner, changed]
    board = New state after the movement
    turn = Turn of the next player
    winner = No one win 0 | Gold wins 1 | Silver wins 2
    changed = True if the state
    """
    board = copy.deepcopy(state)
    if board[origin[0]][origin[1]] == 3:
        isFlag = True
    else:
        isFlag = False
    if turn == 1:
        if isFlag:
            board[position[0]][position[1]] = 3
        else:
            board[position[0]][position[1]] = 1
    else:
        board[position[0]][position[1]] = 2
    board[origin[0]][origin[1]] = 0
    winner = check_winner(board)
    changed = True
    turn = -turn
    return [board, turn, winner, changed]


def make_two_random_moves(state, turns_number, turn):
    """
    Make two random movements for the AI

    :param state: Current state of the game
    :param turns_number: Number of turn that the player have
    :param turn: The turn of the player -1 (silver) | 1 (gold)
    :return: List of two random moves
    """
    board = copy.deepcopy(state)
    isFlag = False
    winner = 0
    moves = []
    first_movement = []
    make_movement = False
    while turns_number > 0 and winner == 0:
        all_positions = get_all_pieces(board, turn)
        if len(all_positions) > 1:
            while not make_movement:
                isFlag = False
                random_position = all_positions[random.randint(0, len(all_positions) - 1)]
                while first_movement == random_position:
                    random_position = all_positions[random.randint(0, len(all_positions) - 1)]
                if board[random_position[0]][random_position[1]] == 3:
                    isFlag = True
                # sometimes the flag moves like a gold piece, check possible_movements
                movements = possible_movements(board, turns_number, random_position, isFlag)
                if len(movements) > 0:
                    make_movement = True
            random_movement = movements[random.randint(0, len(movements) - 1)]
            first_movement = random_movement
            if turn == 1:
                if board[random_movement[0]][random_movement[1]] == 2:
                    turns_number = 0
                if isFlag:
                    board[random_movement[0]][random_movement[1]] = 3
                    turns_number = 0
                else:
                    board[random_movement[0]][random_movement[1]] = 1
            else:
                if (board[random_movement[0]][random_movement[1]] == 1
                        or board[random_movement[0]][random_movement[1]] == 3):
                    turns_number = 0
                board[random_movement[0]][random_movement[1]] = 2
            board[random_position[0]][random_position[1]] = 0
            moves.append((random_position, random_movement))
            turns_number -= 1
            make_movement = False
            isFlag = False
        winner = check_winner(board)
    return moves


def make_random_moves(state, turns_number, turn):
    """
    Make two random movements in the board

    :param state: Current state of the game
    :param turns_number: Number of turn that the player have
    :param turn: The turn of the player -1 (silver) | 1 (gold)
    :return: [board, turn, changed, is_captured, winner]
    board = New state after the movement
    turn = Turn of the next player
    changed = True if the state
    is_captured = True if therandom move is a captured
    winner = No one win 0 | Gold wins 1 | Silver wins 2
    """
    board = copy.deepcopy(state)
    changed = False
    is_captured = False
    isFlag = False
    winner = 0
    first_movement = []
    make_movement = False
    while turns_number > 0 and winner == 0:
        all_positions = get_all_pieces(board, turn)
        if len(all_positions) > 1:
            while not make_movement:
                isFlag = False
                random_position = all_positions[random.randint(0, len(all_positions)-1)]
                while first_movement == random_position:
                    random_position = all_positions[random.randint(0, len(all_positions) - 1)]
                if board[random_position[0]][random_position[1]] == 3:
                    isFlag = True
                movements = possible_movements(board, turns_number, random_position, isFlag)
                if len(movements) > 0:
                    make_movement = True
            random_movement = movements[random.randint(0, len(movements)-1)]
            first_movement = random_movement
            if turn == 1:
                if board[random_movement[0]][random_movement[1]] == 2:
                    is_captured = True
                    turns_number = 0
                if isFlag:
                    board[random_movement[0]][random_movement[1]] = 3
                    turns_number = 0
                else:
                    board[random_movement[0]][random_movement[1]] = 1
            else:
                if (board[random_movement[0]][random_movement[1]] == 1 or board[random_movement[0]][random_movement[1]] == 3):
                    is_captured = True
                    turns_number = 0
                board[random_movement[0]][random_movement[1]] = 2
            board[random_position[0]][random_position[1]] = 0
            changed = True
            turns_number -= 1
            make_movement = False
            isFlag = False
            print("origin:", random_position)
            print("destination:", random_movement)
        winner = check_winner(board)
    turn = -turn
    return [board, turn, changed, is_captured, winner]


def is_end_of_game(state):
    """
    Check if the game is over

    :param state: Current state of the game
    :return: True if the game is over
    """
    if check_winner(state) != 0:
        return True
    else:
        return False


def evaluation_function(state, gold_pieces, silver_pieces, player, depth):
    """
    Evaluate the current state of the game

    :param state: Current state of the game
    :param gold_pieces: Number of gold pieces in the board
    :param silver_pieces: Number of silver pieces in the board
    :param player: Player to analyze (1 = gold | 2 = silver)
    :param depth: Depth of the node that we are evaluated
    :return: value of the node
    """
    # TODO:  If flag can move and is not near from enemies. Random

    result = check_winner(state)

    if result == 0:
        enemy_pieces = 0
        if player == 1:
            enemy = 2
            if silver_pieces > get_enemy_pieces(state, enemy):
                enemy_pieces = 500
        else:
            enemy = 1
            if gold_pieces > get_enemy_pieces(state, enemy):
                enemy_pieces = 500
        block_value = block_flag(state, player) * BLOCK_FLAG
        value = enemy_pieces + block_value
    elif result == player:
        value = MAX_SCORE - 10 * depth
    else:
        value = MAX_SCORE - 10 * depth
    return value


def evaluation_function_nega(state, gold_pieces, silver_pieces, player, depth):
    """
    Evaluate the current state of the game for negamax

    :param state: Current state of the game
    :param gold_pieces: Number of gold pieces in the board
    :param silver_pieces: Number of silver pieces in the board
    :param player: Player to analyze (1 = gold | 2 = silver)
    :param depth: Depth of the node that we are evaluated
    :return: value of the node
    """
    result = check_winner(state)

    if result == 0:
        enemy_pieces = 0
        if player == 1:
            enemy = 2
            if silver_pieces > get_enemy_pieces(state, enemy):
                enemy_pieces = 500
        else:
            enemy = 1
            if gold_pieces > get_enemy_pieces(state, enemy):
                enemy_pieces = 500
        captures_value = future_captures(state, player) * ENEMIES_AROUND
        block_value = block_flag(state, player) * BLOCK_FLAG
        value = enemy_pieces + captures_value + block_value
    elif result == player:
        value = -MAX_SCORE - 10 * depth
    else:
        value = -MAX_SCORE - 10 * depth
    return value


def minmax(state, gold_pieces, silver_pieces, player, turns_number, turn, depth):
    """
    Minimax algorithm

    :param state: Current state of the game
    :param gold_pieces: Number of gold pieces in the board
    :param silver_pieces: Number of silver pieces in the board
    :param player: Player to analyze (1 = gold | 2 = silver)
    :param turns_number: Number of turn that the player have
    :param turn: The turn of the player -1 (silver) | 1 (gold)
    :param depth: Maximum tree depth
    :return: Value of the node
    """
    if (is_end_of_game(state)) or (depth <= 0):
        return evaluation_function(state, gold_pieces, silver_pieces, player, depth)
    moves = generate_moves(state, turns_number, turn)
    value = -INF
    if player == 1:
        orig_turn = 1
    else:
        orig_turn = -1
    for move in moves:
        if len(move) == 2:
            [state, turn, winner, changed] = add_piece_to_table(state, turn, move[0], move[1])
        else:
            [state, turn, winner, changed] = add_two_pieces(state, turn, move)
        if orig_turn != turn:
            value = max(value, minmax(state, gold_pieces, silver_pieces, player, turns_number, turn, depth - 1))
        else:
            value = min(value, minmax(state, gold_pieces, silver_pieces, player, turns_number, turn, depth - 1))
    return value


def alphabeta_negamax(state, gold_pieces, silver_pieces, player, turns_number, turn, depth, alpha, beta):
    """
    Alpha-beta pruning with negamax algorithm

    :param state: Current state of the game
    :param gold_pieces: Number of gold pieces in the board
    :param silver_pieces: Number of silver pieces in the board
    :param player: Player to analyze (1 = gold | 2 = silver)
    :param turns_number: Number of turn that the player have
    :param turn: The turn of the player -1 (silver) | 1 (gold)
    :param depth: Maximum tree depth
    :param alpha: Alpha value
    :param beta: Beta value
    :return: Value of the node
    """
    if (is_end_of_game(state)) or (depth <= 0):
        return evaluation_function_nega(state, gold_pieces, silver_pieces, player, depth)
    moves = generate_moves(state, turns_number, turn)
    score = -INF
    for move in moves:
        if len(move) == 2:
            [state, aux_turn, winner, changed] = add_piece_to_table(state, turn, move[0], move[1])
        else:
            [state, aux_turn, winner, changed] = add_two_pieces(state, turn, move)
        score = max(score, -alphabeta_negamax(state, gold_pieces, silver_pieces, player, turns_number, turn, depth - 1, -beta, -alpha))
        alpha = max(alpha, score)
        if alpha > beta:
            break
    return score


def pvs(state, gold_pieces, silver_pieces, player, turns_number, turn, depth, alpha, beta):
    """
    Principal variation search algorithm

    :param state: Current state of the game
    :param gold_pieces: Number of gold pieces in the board
    :param silver_pieces: Number of silver pieces in the board
    :param player: Player to analyze (1 = gold | 2 = silver)
    :param turns_number: Number of turn that the player have
    :param turn: The turn of the player -1 (silver) | 1 (gold)
    :param depth: Maximum tree depth
    :param alpha: Alpha value
    :param beta: Beta value
    :return:
    """
    if (is_end_of_game(state)) or (depth <= 0):
        return evaluation_function_nega(state, gold_pieces, silver_pieces, player, depth)
    moves = generate_moves(state, turns_number, turn)
    first_child = True
    for move in moves:
        if first_child:
            if len(move) == 2:
                [state, turn, winner, changed] = add_piece_to_table(state, turn, move[0], move[1])
            else:
                [state, turn, winner, changed] = add_two_pieces(state, turn, move)
            score = -pvs(state, gold_pieces, silver_pieces, player, turns_number, turn, depth - 1, -beta, -alpha)
        else:
            if len(move) == 2:
                [state, turn, winner, changed] = add_piece_to_table(state, turn, move[0], move[1])
            else:
                [state, turn, winner, changed] = add_two_pieces(state, turn, move)
            score = -pvs(state, gold_pieces, silver_pieces, player, turns_number, turn, depth - 1, -alpha - 1, -alpha)
            if alpha < score < beta:
                if len(move) == 2:
                    [state, turn, winner, changed] = add_piece_to_table(state, turn, move[0], move[1])
                else:
                    [state, turn, winner, changed] = add_two_pieces(state, turn, move)
                score = -pvs(state, gold_pieces, silver_pieces, player, turns_number, turn, depth - 1, -beta, -score)
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return alpha


def generate_moves(state, turns_number, turn):
    """
    Get possible movements of the board. Get all the pieces and get the
    possible captured movement for each piece.

    get moves or only one move
    [origin, destiny, origin2, destiny2] or [origin, destiny]

    :param state: Current state of the game
    :param turns_number: Number of movements 1 or 2
    :return: List of moves
    """
    positions = []
    moves = []
    more_moves = []
    for i in range(0, 11):
        for j in range(0, 11):
            if (turn == -1 and state[i][j] == 2):
                positions.append([i, j])
            elif (turn == 1 and (state[i][j] == 3 or state[i][j] == 1)):
                positions.append([i, j])
    for origin in positions:
        is_flag = False
        if state[origin[0]][origin[1]] == 3:
            is_flag = True
        for move in possible_one_movements_AI(state, turns_number, turn, origin, is_flag):
            moves.append(move)

    more_moves = generate_all_two_movements(state, turn, positions)
    if len(more_moves) > 100:
        moves = moves + random.sample(more_moves, 100)
    else:
        moves = moves + more_moves
    return moves


def generate_all_two_movements(state, turn, positions):
    """
    Generate two movements for the player

    :param state: Current state of the game
    :param turn: The turn of the player -1 (silver) | 1 (gold)
    :param positions: Positions to analyze
    :return: List of movements
    """
    movements = []
    for position in positions:
        row = position[0]
        column = position[1]
        if state[row][column] != 3:
            for x in range(row, -1, -1):
                if x != row:
                    if state[x][column] == 0:
                        movements = movements + generate_last_move(state, turn, positions, position, [x, column])
                    else:
                        break
            for x in range(row, 11):
                if x != row:
                    if state[x][column] == 0:
                        movements = movements + generate_last_move(state, turn, positions, position, [x, column])
                    else:
                        break
            for y in range(column, -1, -1):
                if y != column:
                    if state[row][y] == 0:
                        movements = movements + generate_last_move(state, turn, positions, position, [row, y])
                    else:
                        break
            for y in range(column, 11):
                if y != column:
                    if state[row][y] == 0:
                        movements = movements + generate_last_move(state, turn, positions, position, [row, y])
                    else:
                        break
    return movements


def generate_last_move(state, turn, positions, origin, destiny):
    """
    Generate the second position of the list of two moves

    :param state: Current state of the game
    :param turn: The turn of the player -1 (silver) | 1 (gold)
    :param positions: Positions to analyze
    :param origin: Origin of the first position
    :param destiny: Destination of the first position
    :return: List of moves
    """
    if turn == 1:
        piece = 1
    else:
        piece = 2
    moves = []
    [new_state, turn_aux, winner, changed] = add_piece_to_table(state, turn, origin, destiny)
    if origin in positions:
        positions.remove(origin)
    for position in positions:
        if position != destiny:
            row = position[0]
            column = position[1]
            if new_state[row][column] != 3:
                for x in range(row, -1, -1):
                    if x != row:
                        if new_state[x][column] == 0:
                            moves.append([origin, destiny, position, [x, column]])
                        else:
                            break
                for x in range(row, 11):
                    if x != row:
                        if new_state[x][column] == 0:
                            moves.append([origin, destiny, position, [x, column]])
                        else:
                            break
                for y in range(column, -1, -1):
                    if y != column:
                        if new_state[row][y] == 0:
                            moves.append([origin, destiny, position, [row, y]])
                        else:
                            break
                for y in range(column, 11):
                    if y != column:
                        if new_state[row][y] == 0:
                            moves.append([origin, destiny, position, [row, y]])
                        else:
                            break
    return moves


def possible_one_movements_AI(state, turns_number, turn, position, isFlag):
    """
    Get the capture movements of the position. If it is the flag, get the movements of the flag

    :param state: Current state of the game
    :param turns_number: Number of movements available
    :param position: Position of the piece that has to be moved
    :param isFlag: True if the position is the flag
    :return: list of movements available in the position
    """
    row = position[0]
    column = position[1]
    piece = state[row][column]
    movements = []
    if turns_number == 2:
        if turn == 1:
            if (in_range([row-1, column-1]) and state[row-1][column-1] == 2):
                movements.append([position, [row-1, column-1]])
            if (in_range([row-1, column+1]) and state[row-1][column+1] == 2):
                movements.append([position, [row-1, column+1]])
            if (in_range([row+1, column-1]) and state[row+1][column-1] == 2):
                movements.append([position, [row+1, column-1]])
            if (in_range([row+1, column+1]) and state[row+1][column+1] == 2):
                movements.append([position, [row+1, column+1]])
        else:
            if (in_range([row-1, column-1]) and state[row-1][column-1] == 1):
                movements.append([position, [row-1, column-1]])
            if (in_range([row-1, column+1]) and state[row-1][column+1] == 1):
                movements.append([position, [row-1, column+1]])
            if (in_range([row+1, column-1]) and state[row+1][column-1] == 1):
                movements.append([position, [row+1, column-1]])
            if (in_range([row+1, column+1]) and state[row+1][column+1] == 1):
                movements.append([position, [row+1, column+1]])
            if (in_range([row-1, column-1]) and state[row-1][column-1] == 3):
                movements.append([position, [row-1, column-1]])
            if (in_range([row-1, column+1]) and state[row-1][column+1] == 3):
                movements.append([position, [row-1, column+1]])
            if (in_range([row+1, column-1]) and state[row+1][column-1] == 3):
                movements.append([position, [row+1, column-1]])
            if (in_range([row+1, column+1]) and state[row+1][column+1] == 3):
                movements.append([position, [row+1, column+1]])
        if isFlag:
            for x in range(row, -1, -1):
                if x != row:
                    if state[x][column] == 0:
                        movements.append([position, [x, column]])
                    else:
                        break
            for x in range(row, 11):
                if x != row:
                    if state[x][column] == 0:
                        movements.append([position, [x, column]])
                    else:
                        break
            for y in range(column, -1, -1):
                if y != column:
                    if state[row][y] == 0:
                        movements.append([position, [row, y]])
                    else:
                        break
            for y in range(column, 11):
                if y != column:
                    if state[row][y] == 0:
                        movements.append([position, [row, y]])
                    else:
                        break
    return movements


def get_all_pieces(state, turn):
    """
    Obtain the positions of every piece

    :param state: Current state of the game
    :param turn: The turn of the player -1 (silver) | 1 (gold)
    :return: List of the positions
    """
    board = copy.deepcopy(state)
    pieces_positions = []
    for row in range(0, 11):
        for column in range(0, 11):
            if turn == 1:
                if board[row][column] == 1 or board[row][column] == 3:
                    pieces_positions.append([row, column])
            elif board[row][column] == 2:
                pieces_positions.append([row, column])
    return pieces_positions


def alphabeta_nega_transposition_table(state, gold_pieces, silver_pieces, player, turns_number, turn, depth, alpha, beta, transposition_table, hashtable):
    """
    Alpha beta negamax with transposition table

    :param state: Current state of the game
    :param gold_pieces: Number of gold pieces in the board
    :param silver_pieces: Number of silver pieces in the board
    :param player: Player to analyze (1 = gold | 2 = silver)
    :param turns_number: Number of turn that the player have
    :param turn: The turn of the player -1 (silver) | 1 (gold)
    :param depth: Maximum tree depth
    :param alpha: Alpha value
    :param beta: Beta value
    :param transposition_table: Transposition table of one player
    :param hashtable: The Hash table
    :return:
    """
    old_alpha = alpha
    best_move = None
    table_entry = retrieve_state_from_table(transposition_table, player, hashtable, state)
    if (table_entry != None) and (table_entry[3] >= depth):
        if table_entry[1] == "exact":
            return table_entry[0]
        elif table_entry[1] == "lower_bound":
            alpha = max(alpha, table_entry[0])
        elif table_entry[1] == "upper_bound":
            beta = min(beta, table_entry[0])
    if (is_end_of_game(state)) or (depth <= 0):
        return evaluation_function_nega(state, gold_pieces, silver_pieces, player, depth)
    moves = generate_moves(state, turns_number, turn)
    best_value = -INF
    for move in moves:
        if len(move) == 2:
            [state, turn, winner, changed] = add_piece_to_table(state, turn, move[0], move[1])
        else:
            [state, turn, winner, changed] = add_two_pieces(state, turn, move)
        best_value = max(best_value, -alphabeta_nega_transposition_table(state, gold_pieces, silver_pieces, player, turns_number, turn, depth - 1, -beta, -alpha, transposition_table, hashtable))
        if best_value >= (MAX_SCORE - 10):
            best_move = move
        alpha = max(alpha, best_value)
        if alpha > beta:
            break
    if best_value <= old_alpha:
        flag = "upper_bound"
    elif best_value >= beta:
        flag = "lower_bound"
    else:
        flag = "exact"
    store_in_table(state, transposition_table, hashtable, best_value, flag, best_move, depth, player)
    return best_value


def get_hashtable_number(coord_pos, player, hashtable):
    """
    Get the value of the coordinate in the hashtable

    :param coord_pos: Coordinate of the board
    :param player: Player to analyze (1 = gold | 2 = silver)
    :param hashtable: The Hash table
    :return: Value of the coordinate in the hashtable
    """
    index_pos = coords_to_linear_pos(coord_pos)
    index_piece = 0
    if player != 1:
        index_piece = 1
    return hashtable[index_piece][index_pos]


def coords_to_linear_pos(coords):
    if coords[0] == 0:
        return coords[1]
    if coords[0] == 1:
        return 1 + coords[1]
    if coords[0] == 2:
        return 1 + 2 + coords[1]
    if coords[0] == 3:
        return 1 + 2 + 3 + coords[1]
    if coords[0] == 4:
        return 1 + 2 + 3 + 4 + coords[1]
    if coords[0] == 5:
        return 1 + 2 + 3 + 4 + 5 + coords[1]
    if coords[0] == 6:
        return 1 + 2 + 3 + 4 + 5 + 6 + coords[1]
    if coords[0] == 7:
        return 1 + 2 + 3 + 4 + 5 + 6 + 7 + coords[1]
    if coords[0] == 8:
        return 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + coords[1]
    if coords[0] == 9:
        return 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + coords[1]
    if coords[0] == 10:
        return 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10 + coords[1]


def retrieve_state_from_table(t_table, player, hashtable, state):
    """
    Get the value of the row in the table

    :param t_table: Transposition table of one player
    :param player: Player to analyze (1 = gold | 2 = silver)
    :param hashtable: The Hash table
    :param state: Current state of the game
    :return: [best_value, flag, best move, depth, hash value]
    """
    hash_coords = 0
    for row in range(0, 11):
        for column in range(0, 11):
            if state[row][column] != 0:
                hash_coords = hash_coords ^ (get_hashtable_number([row, column], player, hashtable))
    for row in t_table:
        if hash_coords == row[-1]:
            return row
    return None


def create_hashtable():
    """
    Generate a hash table(Zobrist) with random bits of 363 sizes

    :return: The hashtable
    """
    n = 121
    m = 3
    temp = [None] * (n * m)
    for i in range(0, len(temp)):
        temp[i] = random.getrandbits(64)
    return [temp[:n], temp[n:]]


def store_in_table(state, transposition_table, table, best_value, flag, best_move, depth, player):
    """
    Store all the positions of the state

    :param state: Current state of the game
    :param transposition_table: Transposition table of one player
    :param table: Best value of the
    :param best_value: The best value
    :param flag: "upper_bound" | "lower_bound" | "exact"
    :param best_move: The best move
    :param depth: Maximum tree depth
    :param player: Player to analyze (1 = gold | 2 = silver)
    :return:
    """
    hash_value = 0
    for row in range(0, 11):
        for column in range(0, 11):
            if state[row][column] != 0:
                hash_value = hash_value ^ (get_hashtable_number([row, column], player, table))
    retrieved = retrieve_state_from_table(transposition_table, player, table, state)
    if retrieved is None:
        transposition_table.append([best_value, flag, best_move, depth, hash_value])
    else:
        if depth > retrieved[3]:
            transposition_table.remove(retrieved)
            transposition_table.append([best_value, flag, best_move, depth, hash_value])
    return transposition_table


