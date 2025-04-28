# Description: Implements Ultimate Tic-Tac-Toe as a CSP for AI-2002 Assignment 03.
#              Models the game with 81 variables (positions), domains {X, O, empty},
#              and constraints (active board rule, no moves on won boards, winning conditions).
#              Uses backtracking search with forward checking for AI moves ('O'),
#              aiming to win fast and block 'X'. Includes a Tkinter GUI for user play ('X').
#              Partially addresses Task 3 (core AI, GUI; experimentation as future work).
#              Handles 3x3 grid of 3x3 boards, with rules for dynamic board selection.

import tkinter as tk
import copy
from tkinter import messagebox

class UltimateTicTacToe:
    """
    Represents the Ultimate Tic-Tac-Toe game state and logic.
    Manages a 3x3 grid of 3x3 boards, enforces rules, and checks wins.
    Used by both GUI and AI solver.
    """
    def __init__(self):
        # Initialize 3x3 grid of 3x3 boards, all empty (' ')
        self.board = [[[[' ' for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        # Track which small boards are won: 'X', 'O', or 'D' (draw), else None
        self.won_boards = [[None for _ in range(3)] for _ in range(3)]
        # Current player: 'X' (user) or 'O' (AI)
        self.current_player = 'X'
        # Last move’s position (i,j,x,y) to determine active board
        self.last_move = None
        # Track game winner: 'X', 'O', or None
        self.winner = None

    def make_move(self, i, j, x, y):
        """
        Attempts to place current player’s mark at position (i,j,x,y).
        Updates state if legal, switches player, and checks wins.
        Args:
            i, j: Small board coordinates (0-2).
            x, y: Position within small board (0-2).
        Returns:
            bool: True if move was made, False if illegal.
        """
        if not self.is_legal_move(i, j, x, y):
            return False
        # Place mark
        self.board[i][j][x][y] = self.current_player
        self.last_move = (i, j, x, y)
        # Check if small board is won
        self.check_small_board_win(i, j)
        # Check if large board is won
        self.check_large_board_win()
        # Switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def is_legal_move(self, i, j, x, y):
        """
        Checks if a move at (i,j,x,y) is legal.
        Enforces active board rule, won boards, and empty cells.
        Args:
            i, j: Small board coordinates.
            x, y: Position within small board.
        Returns:
            bool: True if legal, False otherwise.
        """
        if self.winner or i < 0 or i > 2 or j < 0 or j > 2 or x < 0 or x > 2 or y < 0 or y > 2:
            return False
        # Check if cell is empty
        if self.board[i][j][x][y] != ' ':
            return False
        # Check if small board is won or full
        if self.won_boards[i][j] or self.is_small_board_full(i, j):
            return False
        # Active board rule: next move in board (x,y) from last move
        if self.last_move:
            last_i, last_j, last_x, last_y = self.last_move
            target_board_i, target_board_j = last_x, last_y
            # If target board is won or full, any board is allowed
            if (self.won_boards[target_board_i][target_board_j] or 
                self.is_small_board_full(target_board_i, target_board_j)):
                return True
            # Otherwise, must play in target board
            return i == target_board_i and j == target_board_j
        # First move: any board allowed
        return True

    def is_small_board_full(self, i, j):
        """
        Checks if small board (i,j) is full (no empty cells).
        Args:
            i, j: Small board coordinates.
        Returns:
            bool: True if full, False otherwise.
        """
        for x in range(3):
            for y in range(3):
                if self.board[i][j][x][y] == ' ':
                    return False
        return True

    def check_small_board_win(self, i, j):
        """
        Checks if small board (i,j) is won by 'X' or 'O', or drawn.
        Updates won_boards[i][j] if won or full.
        Args:
            i, j: Small board coordinates.
        """
        board = self.board[i][j]
        # Check rows, columns, diagonals
        for k in range(3):
            # Row
            if board[k][0] == board[k][1] == board[k][2] != ' ':
                self.won_boards[i][j] = board[k][0]
                return
            # Column
            if board[0][k] == board[1][k] == board[2][k] != ' ':
                self.won_boards[i][j] = board[0][k]
                return
        # Diagonals
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            self.won_boards[i][j] = board[0][0]
            return
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            self.won_boards[i][j] = board[0][2]
            return
        # Check draw
        if self.is_small_board_full(i, j):
            self.won_boards[i][j] = 'D'

    def check_large_board_win(self):
        """
        Checks if the large board is won by 'X' or 'O', or drawn.
        Updates winner if won, checks if game is drawn.
        """
        # Check rows, columns, diagonals
        for k in range(3):
            # Row
            if (self.won_boards[k][0] == self.won_boards[k][1] == 
                self.won_boards[k][2] and self.won_boards[k][0] in ['X', 'O']):
                self.winner = self.won_boards[k][0]
                return
            # Column
            if (self.won_boards[0][k] == self.won_boards[1][k] == 
                self.won_boards[2][k] and self.won_boards[0][k] in ['X', 'O']):
                self.winner = self.won_boards[0][k]
                return
        # Diagonals
        if (self.won_boards[0][0] == self.won_boards[1][1] == 
            self.won_boards[2][2] and self.won_boards[0][0] in ['X', 'O']):
            self.winner = self.won_boards[0][0]
            return
        if (self.won_boards[0][2] == self.won_boards[1][1] == 
            self.won_boards[2][0] and self.won_boards[0][2] in ['X', 'O']):
            self.winner = self.won_boards[0][2]
            return
        # Check draw: all boards won or full
        all_done = True
        for i in range(3):
            for j in range(3):
                if not (self.won_boards[i][j] or self.is_small_board_full(i, j)):
                    all_done = False
                    break
        if all_done:
            self.winner = 'D'

    def is_game_over(self):
        """
        Checks if the game is over (won or drawn).
        Returns:
            bool: True if over, False otherwise.
        """
        return self.winner is not None

    def get_legal_moves(self):
        """
        Generates all legal moves based on active board rule.
        Returns:
            list: List of (i,j,x,y) tuples for legal moves.
        """
        moves = []
        if self.is_game_over():
            return moves
        # Determine active board
        active_i, active_j = None, None
        if self.last_move:
            _, _, last_x, last_y = self.last_move
            active_i, active_j = last_x, last_y
            # If active board is won or full, any board allowed
            if (self.won_boards[active_i][active_j] or 
                self.is_small_board_full(active_i, active_j)):
                active_i, active_j = None, None
        # Generate moves
        for i in range(3):
            for j in range(3):
                # Skip if board is won or full
                if self.won_boards[i][j] or self.is_small_board_full(i, j):
                    continue
                # Check active board rule
                if active_i is not None and (i != active_i or j != active_j):
                    continue
                for x in range(3):
                    for y in range(3):
                        if self.board[i][j][x][y] == ' ':
                            moves.append((i, j, x, y))
        return moves

    def can_win_immediately(self, player):
        """
        Checks if player can win with one move (small or large board).
        Used for forward checking.
        Args:
            player: 'X' or 'O'.
        Returns:
            tuple: (i,j,x,y) of winning move, or None if none exists.
        """
        original_player = self.current_player
        self.current_player = player
        for i, j, x, y in self.get_legal_moves():
            # Simulate move
            temp_board = copy.deepcopy(self.board)
            temp_won = copy.deepcopy(self.won_boards)
            temp_winner = self.winner
            self.board[i][j][x][y] = player
            self.check_small_board_win(i, j)
            self.check_large_board_win()
            if self.winner == player:
                # Undo move
                self.board = temp_board
                self.won_boards = temp_won
                self.winner = temp_winner
                self.current_player = original_player
                return (i, j, x, y)
            # Undo move
            self.board = temp_board
            self.won_boards = temp_won
            self.winner = temp_winner
        self.current_player = original_player
        return None

    def minimax_with_forward_checking(self, depth, max_depth, maximizing):
        """
        Implements backtracking search with forward checking.
        Evaluates game state, prunes branches where opponent wins immediately.
        Args:
            depth: Current recursion depth.
            max_depth: Maximum depth to explore.
            maximizing: True for 'X' (maximizing), False for 'O' (minimizing).
        Returns:
            int: Score (1 for X win, -1 for O win, 0 for draw or heuristic).
        """
        if self.is_game_over():
            if self.winner == 'X':
                return 1
            elif self.winner == 'O':
                return -1
            return 0
        if depth >= max_depth:
            # Heuristic: difference in won small boards
            x_wins = sum(row.count('X') for row in self.won_boards)
            o_wins = sum(row.count('O') for row in self.won_boards)
            return (x_wins - o_wins) / 10  # Normalize to [-1, 1]

        legal_moves = self.get_legal_moves()
        if not legal_moves:
            return 0

        if maximizing:
            max_score = float('-inf')
            for i, j, x, y in legal_moves:
                # Forward checking: skip if O can win immediately after
                temp_game = copy.deepcopy(self)
                temp_game.make_move(i, j, x, y)
                if temp_game.can_win_immediately('O'):
                    continue
                score = temp_game.minimax_with_forward_checking(depth + 1, max_depth, False)
                max_score = max(max_score, score)
            return max_score
        else:
            min_score = float('inf')
            for i, j, x, y in legal_moves:
                # Forward checking: skip if X can win immediately after
                temp_game = copy.deepcopy(self)
                temp_game.make_move(i, j, x, y)
                if temp_game.can_win_immediately('X'):
                    continue
                score = temp_game.minimax_with_forward_checking(depth + 1, max_depth, True)
                min_score = min(min_score, score)
            return min_score

    def get_best_move_for_player(self, player, max_depth=3):
        """
        Finds the best move for the given player using minimax with forward checking.
        Args:
            player: 'X' or 'O'.
            max_depth: Maximum search depth (default 3 for performance).
        Returns:
            tuple: (i,j,x,y) of best move, or None if no moves.
        """
        original_player = self.current_player
        self.current_player = player
        legal_moves = self.get_legal_moves()
        if not legal_moves:
            self.current_player = original_player
            return None

        # Check for immediate win
        immediate_win = self.can_win_immediately(player)
        if immediate_win:
            self.current_player = original_player
            return immediate_win

        best_score = float('-inf') if player == 'X' else float('inf')
        best_move = None
        for i, j, x, y in legal_moves:
            temp_game = copy.deepcopy(self)
            temp_game.make_move(i, j, x, y)
            # Forward checking
            opponent = 'O' if player == 'X' else 'X'
            if temp_game.can_win_immediately(opponent):
                continue
            score = temp_game.minimax_with_forward_checking(0, max_depth, player == 'O')
            if player == 'X' and score > best_score:
                best_score = score
                best_move = (i, j, x, y)
            elif player == 'O' and score < best_score:
                best_score = score
                best_move = (i, j, x, y)
        self.current_player = original_player
        return best_move

class UltimateTicTacToeGUI:
    """
    Implements a Tkinter GUI for Ultimate Tic-Tac-Toe.
    Displays a 3x3 grid of 3x3 boards, handles user clicks ('X'),
    and triggers AI moves ('O'). Updates board and shows turns.
    """
    def __init__(self, root):
        """
        Initializes the GUI with a canvas and game instance.
        Args:
            root: Tkinter root window.
        """
        self.root = root
        self.root.title("Ultimate Tic-Tac-Toe")
        self.game = UltimateTicTacToe()
        # Canvas: 600x600 pixels for 3x3 grid of 200x200 small boards
        self.canvas = tk.Canvas(root, width=600, height=600, bg='white')
        self.canvas.pack()
        # Label to show current player’s turn
        self.turn_label = tk.Label(root, text="Your turn (X)", font=("Arial", 14))
        self.turn_label.pack()
        # Bind mouse clicks to handle user moves
        self.canvas.bind("<Button-1>", self.on_click)
        # Draw initial board
        self.draw_board()
        self.update_board()

    def draw_board(self):
        """
        Draws the 3x3 large grid and 3x3 small grids.
        Large grid: 200x200 per board, small grid: ~66.67x66.67 per cell.
        """
        # Large grid lines
        for k in range(1, 3):
            # Vertical
            self.canvas.create_line(k * 200, 0, k * 200, 600, width=3)
            # Horizontal
            self.canvas.create_line(0, k * 200, 600, k * 200, width=3)
        # Small grid lines
        for i in range(3):
            for j in range(3):
                # Base coordinates for small board
                base_x, base_y = j * 200, i * 200
                # Draw 3x3 grid
                for k in range(1, 3):
                    # Vertical
                    self.canvas.create_line(base_x + k * 66.67, base_y, 
                                           base_x + k * 66.67, base_y + 200, width=1)
                    # Horizontal
                    self.canvas.create_line(base_x, base_y + k * 66.67, 
                                           base_x + 200, base_y + k * 66.67, width=1)

    def update_board(self):
        """
        Updates the canvas to reflect current board state.
        Draws 'X' and 'O' marks, highlights won boards.
        """
        # Clear previous marks
        self.canvas.delete("mark")
        for i in range(3):
            for j in range(3):
                for x in range(3):
                    for y in range(3):
                        mark = self.game.board[i][j][x][y]
                        if mark == ' ':
                            continue
                        # Center of cell
                        cell_x = j * 200 + y * 66.67 + 33.33
                        cell_y = i * 200 + x * 66.67 + 33.33
                        if mark == 'X':
                            # Draw X
                            self.canvas.create_line(
                                cell_x - 20, cell_y - 20, cell_x + 20, cell_y + 20,
                                fill='blue', width=2, tags="mark")
                            self.canvas.create_line(
                                cell_x + 20, cell_y - 20, cell_x - 20, cell_y + 20,
                                fill='blue', width=2, tags="mark")
                        else:  # O
                            # Draw O
                            self.canvas.create_oval(
                                cell_x - 20, cell_y - 20, cell_x + 20, cell_y + 20,
                                outline='red', width=2, tags="mark")
                # Highlight won boards
                if self.game.won_boards[i][j] in ['X', 'O']:
                    base_x, base_y = j * 200, i * 200
                    color = 'blue' if self.game.won_boards[i][j] == 'X' else 'red'
                    self.canvas.create_rectangle(
                        base_x + 5, base_y + 5, base_x + 195, base_y + 195,
                        outline=color, width=4, tags="mark")

    def on_click(self, event):
        """
        Handles mouse clicks on the canvas.
        Places 'X' for user, triggers AI move ('O'), updates GUI.
        Args:
            event: Tkinter event with x, y coordinates.
        """
        if self.game.current_player != 'X' or self.game.is_game_over():
            return
        # Map click to (i,j,x,y)
        x, y = event.y, event.x  # Canvas coordinates
        i = x // 200  # Small board row
        j = y // 200  # Small board column
        # Position within small board
        cell_x = (x % 200) / 66.67
        cell_y = (y % 200) / 66.67
        x_idx = int(cell_x)
        y_idx = int(cell_y)
        # Attempt user move
        if self.game.make_move(i, j, x_idx, y_idx):
            self.update_board()
            self.check_game_status()
            # Update turn label
            self.turn_label.config(text="AI's turn (O)")
            # Trigger AI move
            self.root.after(100, self.ai_move)

    def ai_move(self):
        """
        Executes AI move for 'O' using minimax with forward checking.
        Updates board and checks game status.
        """
        if self.game.current_player != 'O' or self.game.is_game_over():
            return
        move = self.game.get_best_move_for_player('O', max_depth=3)
        if move:
            i, j, x, y = move
            self.game.make_move(i, j, x, y)
            self.update_board()
            self.check_game_status()
            self.turn_label.config(text="Your turn (X)")

    def check_game_status(self):
        """
        Checks if the game is over and shows a message box if won or drawn.
        """
        if self.game.is_game_over():
            if self.game.winner == 'X':
                messagebox.showinfo("Game Over", "You win!")
            elif self.game.winner == 'O':
                messagebox.showinfo("Game Over", "AI wins!")
            else:
                messagebox.showinfo("Game Over", "It's a draw!")
            self.root.quit()

def main():
    """
    Main function to launch the Ultimate Tic-Tac-Toe GUI.
    Creates Tkinter window and starts the game.
    """
    root = tk.Tk()
    app = UltimateTicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()