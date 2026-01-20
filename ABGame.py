import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import MorrisBasics as m

# Global variable to track positions evaluated
positionsEvaluated = 0

# The brain of the AI.
def ABGame(boardString, depth, alpha, beta, isMaximizingPlayer):

    global positionsEvaluated

    if depth == 0:
        positionsEvaluated += 1
        return m.static_estimation(boardString, False, True), None
    
    if isMaximizingPlayer:
        # White's turn - maximize
        max_eval = float("-inf")
        best_move = None

        # Generate all possible moves for white
        possible_moves = m.GenerateMove("W",boardString)

        for move in possible_moves:
            eval_score, _ = ABGame(move, depth - 1, alpha, beta, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
        
        return max_eval, best_move
    
    else:
        # Black's turn - minimize
        min_eval = float("inf")
        best_move = None

        # Generate all possible moves for black by flipping the board
        possible_moves = m.GenerateMove("W",m.flipBoard(boardString))

        for move in possible_moves:
            # Generate black moves by making it modular in a different function!
            move = m.flipBoard(move)
            eval_score, _ = ABGame(move, depth - 1, alpha, beta, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, eval_score)
            if beta <= alpha:
                break

        return min_eval, best_move

def main():
    global positionsEvaluated
    positionsEvaluated = 0  # Reset counter for each run
    
    # Check if command line arguments are provided
    if len(sys.argv) == 4:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        depth = int(sys.argv[3])
    else:
        # Default values
        input_file = r"D:/AI/Project_0/board1.txt"
        output_file = r"D:/AI/Project_0/board2.txt"
        depth = 2
    
    initial_board = m.read_board_from_file(input_file)    
    eval_score, best_move = ABGame(m.board_to_string(initial_board), depth, float("-inf"), float("inf"), True)

    # Add null check for best_move
    if best_move is not None:
        print(f"Board Position: {m.board_to_string(best_move)}")
        m.write_board_to_file(best_move, output_file)
    else:
        print("No valid moves found!")
        
    print("Positions Evaluated by Static Estimation: ", positionsEvaluated)
    print("AB estimate: ", eval_score)


if __name__ == "__main__":
    main()