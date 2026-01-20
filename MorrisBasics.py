import sys

# This function generates all possible combinations of adding a white piece to the board.
def GenerateAdd(boardString):
    copyBoardString = boardString
    possibleCombination = []    

    for i in range(len(boardString)):
        if(boardString[i] == "x"):
            copyBoardString = boardString[:i] + "W" + boardString[i+1:]
            if(closeMill("W", copyBoardString, i)):
                # print("Close Mill for White at position: ", i)
                temp = GenerateRemove(copyBoardString)
                for arr in temp:
                    possibleCombination.append(arr)
                # possibleCombination.append(GenerateRemove(copyBoardString))
            else:
                possibleCombination.append(copyBoardString)

    # Debug line
    # print(len(possibleCombination))
    # Debug line
    return possibleCombination

def GenerateRemove(boardString):    
    possibleCombination = []

    # This is removing B only. 
    for i in range(len(boardString)):
        if(boardString[i] == "B" and not closeMill("B", boardString, i)):            
            possibleCombination.append(boardString[:i] + "x" + boardString[i+1:])

    return possibleCombination
    
# The function can check if either black or white has a mill. For now we call it for white but to call it for black, the board can be mirrored and called for white.
def closeMill(piece,boardString,location):

    MILLS = [ #all possible mills
        #Vertical Mills
        [0,6,18],
        [2,7,15],
        [4,8,12],
        [13,16,19],
        [5,9,14],
        [3,10,17],
        [1,11,20],
        #Horizontal Mills
        [6,7,8],
        [9,10,11],
        [12,13,14],
        [15,16,17],
        [18,19,20],
        #Diagonal Mills
        [0,2,4],
        [12,15,18],
        [14,17,20],
        [1,3,5]
    ]

    piece = piece*3  # Ensure piece is uppercase for consistency
    
    for mill in MILLS:
        if location in mill:            
            i = 0
            str = ""
            for i in range(3):
                str += boardString[mill[i]]            
            if(str == piece):
                return True        
    return False

def GenerateMove(piece,boardString):
    # Existing piece should be moved to all possible empty positions.
    
    # The below map is used to find if you are at 'x' position, where can you move your respective piece. This imitates the neighbors function in the assignment. 
    map_allowed_legal_positions = {
        0: [1,2,6], 
        1: [0,3,11],
        2: [0,3,4,7],
        3: [1,2,5,10],
        4: [2,5,8],
        5: [3,4,9],
        6: [0,7,18],
        7: [2,6,8,15],
        8: [4,7,12],
        9: [5,10,14],
        10: [3,9,11,17],
        11: [1,10,20],
        12: [8,13,15],
        13: [12,14,16],
        14: [9,13,17],
        15: [7,12,16,18],
        16: [13,15,17,19],
        17: [10,14,16,20],
        18: [6,15,19],
        19: [16,18,20],
        20: [11,17,19]
    }

    white_count = boardString.count("W")
    notPiece = "B" if piece == "W" else "W"

    if(white_count == 3 and piece == "W"):
        return GenerateHopping("W", boardString)
    else:

        L = []

        for i in range(len(boardString)):
            if(boardString[i] == piece):

                adjacent_positions = map_allowed_legal_positions[i]

                for val in adjacent_positions:
                    if boardString[val] == "x":
                        boardStringList = list(boardString)
                        boardStringList[i], boardStringList[val] = boardStringList[val], boardStringList[i]  # Swap the pieces
                        copyBoardString = "".join(boardStringList)
                        if(closeMill(piece, copyBoardString, val)):
                            # print("Close Mill for", piece, "at position:", val)
                            temp = GenerateRemove(copyBoardString)
                            for arr in temp:
                                L.append(arr)
                        else:
                            L.append(copyBoardString)
        return L

def GenerateHopping(piece,boardString):
    # print("Hopping")
    L = []

    # print("Generating Hopping for piece: ", piece)
    for i in range(len(boardString)):
        if(boardString[i] == piece):
            for j in range(len(boardString)):
                if(boardString[j] == "x" and i != j):
                    copy = list(boardString)
                    copy[i] = "x"
                    copy[j] = piece
                    L.append("".join(copy))
    # print("Generated Hopping Moves: ", L)                    
    return L

def staticEstimate(boardString, isOpening):
    numWhitePieces = boardString.count("W")
    numBlackPieces = boardString.count("B")
    
    if isOpening:
        return numWhitePieces - numBlackPieces
    
    if numBlackPieces <= 2:
        return 10000
    elif numWhitePieces <= 2:
        return -10000
    
    black_moves = GenerateAdd(flipBoard(boardString))

    for i in len(black_moves):
        black_moves[i] = flipBoard(black_moves[i])
    
    numBlackMoves = len(black_moves)

    if numBlackMoves == 0:
        return 10000
    
    return 1000 * (numWhitePieces - numBlackPieces) - numBlackMoves


    if depth == 0:
        return staticEstimate(boardString)

    if isMaximizingPlayer:
        max_eval = float("-inf")
        best_move = None

        # Generate all possible moves for white
        possible_moves = GenerateMove("W",boardString)

        for move in possible_moves:
            eval_score, _ = minimaxMidgame_Endgame(move, depth - 1, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move

    else:
        min_eval = float("inf")
        best_move = None

        # Generate all possible moves for black
        possible_moves = GenerateMove("B",flipBoard(boardString))

        for move in possible_moves:
            move = flipBoard(move)
            eval_score, _ = minimaxMidgame_Endgame(move, depth - 1, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

        return min_eval, best_move

def flipBoard(boardString):
    return "".join(["B" if char == "W" else "W" if char == "B" else char for char in boardString])

def read_board_from_file(filename):
    try:
        with open(filename, "r") as file:
            content = file.read().strip()
            return list(content)
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        sys.exit(1)

def write_board_to_file(board, filename):
    try:
        with open(filename, "w") as file:
            file.write("".join(board))
    except IOError:
        print(f"Error: Could not write to file {filename}")
        sys.exit(1)

def board_to_string(board):
    """
    Converts board list to string
    """
    return "".join(board)

########### MY STATIC ESTIMATE FUNCTION ###########



def BetterStaticEstimate(boardString, isOpening):
    numWhitePieces = boardString.count("W")
    numBlackPieces = boardString.count("B")
    numWhiteMills = countMills(boardString, "W")
    numBlackMills = countMills(boardString, "B")
    numWhiteBlocked = countBlockedPieces(boardString, "W")
    numBlackBlocked = countBlockedPieces(boardString, "B")

    if isOpening:
        # Opening: prioritize piece difference and potential mills
        return 10 * (numWhitePieces - numBlackPieces) + 5 * (numWhiteMills - numBlackMills)

    if numBlackPieces <= 2:
        return 10000
    elif numWhitePieces <= 2:
        return -10000

    # Generate all possible black moves (after flipping)
    black_moves = GenerateMove("W", flipBoard(boardString))
    numBlackMoves = len(black_moves)

    if numBlackMoves == 0:
        return 10000

    # Heuristic: piece diff, mills, blocked opponent, mobility, blocked own
    return (
        1000 * (numWhitePieces - numBlackPieces)
        + 500 * (numWhiteMills - numBlackMills)
        + 200 * (numBlackBlocked - numWhiteBlocked)
        - 10 * numBlackMoves
    )        

def countMills(boardString, piece):
    MILLS = [
        [0,6,18], [2,7,15], [4,8,12], [13,16,19], [5,9,14], [3,10,17], [1,11,20],
        [6,7,8], [9,10,11], [12,13,14], [15,16,17], [18,19,20],
        [0,2,4], [12,15,18], [14,17,20], [1,3,5]
    ]
    count = 0
    for mill in MILLS:
        # Only count mills where all indices are within the boardString length
        if all(0 <= pos < len(boardString) and boardString[pos] == piece for pos in mill):
            count += 1
    return count

def countBlockedPieces(boardString, piece):
    map_allowed_legal_positions = {
        0: [1,2,6], 1: [0,3,11], 2: [0,3,4,7], 3: [1,2,5,10], 4: [2,5,8], 5: [3,4,9],
        6: [0,7,18], 7: [2,6,8,15], 8: [4,7,12], 9: [5,10,14], 10: [3,9,11,17],
        11: [1,10,20], 12: [8,13,15], 13: [12,14,16], 14: [9,13,17],
        15: [7,12,16,18], 16: [13,15,17,19], 17: [10,14,16,20], 18: [6,15,19],
        19: [16,18,20], 20: [11,17,19]
    }
    blocked = 0
    for i in range(len(boardString)):
        if boardString[i] == piece:
            neighbors = map_allowed_legal_positions.get(i, [])
            if all(boardString[n] != "x" for n in neighbors):
                blocked += 1
    return blocked

# Best Static Integration
def static_estimation(board, is_opening_phase, is_white_role):
    # board: string of length 21
    # mills: list of mill triplets (MILLS list)
    # is_opening_phase: bool
    # is_white_role: bool (True if evaluating as white)

    player = 'W' if is_white_role else 'B'
    opponent = 'B' if is_white_role else 'W'

    player_pieces = board.count(player)
    opponent_pieces = board.count(opponent)

    # Basic counts
    player_mills = count_mills(board, player)
    opponent_mills = count_mills(board, opponent)

    player_double_threats = count_double_threats(board, player)
    opponent_double_threats = count_double_threats(board, opponent)

    player_block_moves = count_blocked_pieces(board, opponent)  # how many opp moves are blocked

    # Weights tuned per role
    if is_white_role:
        W_mill = 30
        W_double_threat = 40
        W_block = 15
    else:
        W_mill = 25
        W_double_threat = 20
        W_block = 45  # much higher for blocking as black

    # Opening vs Mid/Endgame
    if is_opening_phase:
        score = (
            5 * player_pieces
            + W_mill * player_mills
            + W_double_threat * player_double_threats
            + W_block * player_block_moves
            - (W_block * opponent_double_threats)  # penalize letting opponent get double threats
        )
    else:
        mobility = count_possible_moves(board, player)
        score = (
            10 * player_pieces
            + W_mill * player_mills
            + W_double_threat * player_double_threats
            + W_block * player_block_moves
            + 8 * mobility
            - (W_block * opponent_double_threats)
        )

    return score



# --- Helper Function Stubs ---

def count_mills(boardString, color):
    """Return the number of completed mills for the given color."""

    # This function should count the number of mills for the specified color
    
    MILLS = [
        #Vertical Mills
        [0,6,18],
        [2,7,15],
        [4,8,12],
        [13,16,19],
        [5,9,14],
        [3,10,17],
        [1,11,20],
        #Horizontal Mills
        [6,7,8],
        [9,10,11],
        [12,13,14],
        [15,16,17],
        [18,19,20],
        #Diagonal Mills
        [0,2,4],
        [12,15,18],
        [14,17,20],
        [1,3,5]
    ]

    count = 0

    for mill in MILLS:
        str = ""
        for pos in mill:
            str += boardString[pos]
        if str == color * 3:
            count += 1
    
    return count

def count_two_in_row(boardString, color):
    """Return the number of lines with exactly two pieces of 'color' and one empty."""
    MILLS = [
        #Vertical Mills
        [0,6,18],
        [2,7,15],
        [4,8,12],
        [13,16,19],
        [5,9,14],
        [3,10,17],
        [1,11,20],
        #Horizontal Mills
        [6,7,8],
        [9,10,11],
        [12,13,14],
        [15,16,17],
        [18,19,20],
        #Diagonal Mills
        [0,2,4],
        [12,15,18],
        [14,17,20],
        [1,3,5]
    ]

    count = 0

    for mill in MILLS:
        str = ""
        for pos in mill:
            str += boardString[pos]
        if str.count(color) == 2 and str.count("x") == 1:
            count += 1
    return count
            

def count_double_threats(boardString, player_color):
    """
    Count immediate and setup double threats for player_color.

    board_str: string, each character represents a position
               'W' = White, 'B' = Black, '-' = Empty
    player_color: 'W' or 'B'
    mills: list of lists, each sublist has 3 integers representing positions of a mill
    """

    opponent = 'B' if player_color == 'W' else 'W'
    immediate_threats = 0
    setup_threats = 0

    MILLS = [
        #Vertical Mills
        [0,6,18],
        [2,7,15],
        [4,8,12],
        [13,16,19],
        [5,9,14],
        [3,10,17],
        [1,11,20],
        #Horizontal Mills
        [6,7,8],
        [9,10,11],
        [12,13,14],
        [15,16,17],
        [18,19,20],
        #Diagonal Mills
        [0,2,4],
        [12,15,18],
        [14,17,20],
        [1,3,5]
    ]


    double_threat_count = 0

    # Loop through each possible mill
    for i, mill1 in enumerate(MILLS):
        for j, mill2 in enumerate(MILLS):
            if j <= i:
                continue  # avoid duplicate pairs

            # Find common position between the two mills
            common = list(set(mill1) & set(mill2))
            if len(common) != 1:
                continue  # double threat must share exactly one position

            common_pos = common[0]
            other1 = [p for p in mill1 if p != common_pos]
            other2 = [p for p in mill2 if p != common_pos]

            # Check if the shared position + both other positions are empty
            if boardString[common_pos] == 'x' and all(boardString[pos] == 'x' for pos in other1 + other2):
                # This means if player takes common_pos now, they can complete either mill1 or mill2 later
                double_threat_count += 1

    return double_threat_count


def count_blocked_pieces(boardString, color):
    """Return the number of pieces of 'color' that cannot move."""
    # The below map is used to find if you are at 'x' position, where can you move your respective piece. This imitates the neighbors function in the assignment. 
    adjacent_positions = {
        0: [1,2,6], 
        1: [0,3,11],
        2: [0,3,4,7],
        3: [1,2,5,10],
        4: [2,5,8],
        5: [3,4,9],
        6: [0,7,18],
        7: [2,6,8,15],
        8: [4,7,12],
        9: [5,10,14],
        10: [3,9,11,17],
        11: [1,10,20],
        12: [8,13,15],
        13: [12,14,16],
        14: [9,13,17],
        15: [7,12,16,18],
        16: [13,15,17,19],
        17: [10,14,16,20],
        18: [6,15,19],
        19: [16,18,20],
        20: [11,17,19]
    }
    
    count = 0

    for key in adjacent_positions:
        str = ""
        if boardString[key] == color:
            for values in adjacent_positions[key]:
                str += boardString[values]
            if str.count("x") == 0:
                count += 1
    return count


def count_moves(boardString, color):
    # The below map is used to find if you are at 'x' position, where can you move your respective piece. This imitates the neighbors function in the assignment. 
    adjacent_positions = {
        0: [1,2,6], 
        1: [0,3,11],
        2: [0,3,4,7],
        3: [1,2,5,10],
        4: [2,5,8],
        5: [3,4,9],
        6: [0,7,18],
        7: [2,6,8,15],
        8: [4,7,12],
        9: [5,10,14],
        10: [3,9,11,17],
        11: [1,10,20],
        12: [8,13,15],
        13: [12,14,16],
        14: [9,13,17],
        15: [7,12,16,18],
        16: [13,15,17,19],
        17: [10,14,16,20],
        18: [6,15,19],
        19: [16,18,20],
        20: [11,17,19]
    }
    
    count = 0

    for key in adjacent_positions:
        if boardString[key] == color:
            for values in adjacent_positions[key]:
                if boardString[values] == "x":
                    count += 1
    return count

def count_possible_moves(board, player):

    adjacency_list = {
        0: [1,2,6], 
        1: [0,3,11],
        2: [0,3,4,7],
        3: [1,2,5,10],
        4: [2,5,8],
        5: [3,4,9],
        6: [0,7,18],
        7: [2,6,8,15],
        8: [4,7,12],
        9: [5,10,14],
        10: [3,9,11,17],
        11: [1,10,20],
        12: [8,13,15],
        13: [12,14,16],
        14: [9,13,17],
        15: [7,12,16,18],
        16: [13,15,17,19],
        17: [10,14,16,20],
        18: [6,15,19],
        19: [16,18,20],
        20: [11,17,19]
        }

    moves = 0
    for pos, piece in enumerate(board):
        if piece == player:
            for neighbor in adjacency_list[pos]:
                if board[neighbor] == 'x':
                    moves += 1
    return moves