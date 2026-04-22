import os
import json
import sqlite3
import hashlib
import uuid
from datetime import datetime
from enum import Enum
import tkinter as tk
from tkinter import messagebox, simpledialog


class GameState(Enum):
    """Enumeration for different game states.
    
    Attributes:
        MENU: Main menu state
        LOGIN: Login/post-login state
        PLAYING: Active game state
        GAME_OVER: Game finished state
    """
    MENU = 1
    LOGIN = 2
    PLAYING = 3
    GAME_OVER = 4

class TicTacToe:
    """A Tic Tac Toe game application with user authentication and game persistence.
    
    This class implements a GUI-based Tic Tac Toe game using tkinter with SQLite
    database backend for user management and game history tracking. Players can
    create accounts, authenticate, play against each other, and save/load games.
    
    Attributes:
        root (tk.Tk): The root tkinter window
        db_path (str): Path to the SQLite database file
        savegame_folder (str): Directory for saving game states
        current_user (str): Currently logged-in username
        opponent (str): Current opponent username
        board (list): 9-element list representing the game board
        current_player (str): 'X' or 'O' representing whose turn it is
        game_state (GameState): Current state of the game
        game_id (str): Unique identifier for current game
        buttons (list): List of tkinter button widgets for the board
    """
    
    def __init__(self, root):
        """Initialize the Tic Tac Toe application.
        
        Args:
            root (tk.Tk): The root tkinter window
        """
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("400x500")
        
        self.db_path = "tictactoe.db"
        self.savegame_folder = "savegames"
        self.current_user = None
        self.opponent = None
        self.board = [' '] * 9
        self.current_player = 'X'
        self.game_state = GameState.MENU
        self.game_id = None
        self.buttons = []
        
        self._init_db()
        self._init_savegame_folder()
        self.show_main_menu()
    
    def _init_db(self):
        """Initialize SQLite database with users and games tables.
        
        Creates two tables if they don't exist:
            - users: Stores username, password hash, and statistics
            - games: Stores game records with player info and results
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS games (
            id TEXT PRIMARY KEY,
            player_x TEXT NOT NULL,
            player_o TEXT NOT NULL,
            winner TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(player_x) REFERENCES users(username),
            FOREIGN KEY(player_o) REFERENCES users(username)
        )''')
        
        conn.commit()
        conn.close()
    
    def _init_savegame_folder(self):
        """Create savegames folder if it doesn't exist."""
        if not os.path.exists(self.savegame_folder):
            os.makedirs(self.savegame_folder)
    
    def _hash_password(self, password):
        """Hash password using MD5 algorithm.
        
        Args:
            password (str): Plain text password to hash
            
        Returns:
            str: MD5 hexadecimal hash of the password
        """
        return hashlib.md5(password.encode()).hexdigest()
    
    def clear_frame(self):
        """Clear all widgets from the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_account(self, username, password):
        """Create a new user account in the database.
        
        Args:
            username (str): Desired username
            password (str): Desired password (will be hashed)
            
        Returns:
            bool: True if account created successfully, False if username exists
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            password_hash = self._hash_password(password)
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                         (username, password_hash))
            conn.commit()
            messagebox.showinfo("Success", f"Account '{username}' created successfully!")
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
            return False
        finally:
            conn.close()
    
    def authenticate_user(self, username, password):
        """Authenticate user credentials against database.
        
        Args:
            username (str): Username to authenticate
            password (str): Password to verify
            
        Returns:
            bool: True if credentials are valid, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self._hash_password(password)
        cursor.execute('SELECT username FROM users WHERE username = ? AND password_hash = ?',
                      (username, password_hash))
        result = cursor.fetchone()
        conn.close()
        
        return result is not None
    
    def is_winner(self, player):
        """Check if a player has won the game.
        
        Args:
            player (str): 'X' or 'O'
            
        Returns:
            bool: True if player has three in a row, False otherwise
        """
        winning_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combos:
            if all(self.board[i] == player for i in combo):
                return True
        return False
    
    def is_board_full(self):
        """Check if the game board is completely filled.
        
        Returns:
            bool: True if no empty spaces remain, False otherwise
        """
        return ' ' not in self.board
    
    def make_move(self, position):
        """Make a move at the specified board position.
        
        Args:
            position (int): Board position (0-8)
            
        Returns:
            bool: True if move was valid and made, False otherwise
        """
        if position < 0 or position > 8:
            return False
        if self.board[position] != ' ':
            return False
        
        self.board[position] = self.current_player
        return True
    
    def switch_player(self):
        """Switch current player between 'X' and 'O'."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def save_game(self):
        """Save current game state to a JSON file.
        
        Creates a JSON file in the savegames folder with board state, player info,
        and timestamp. Displays success message with game ID.
        """
        self.game_id = str(uuid.uuid4())
        save_data = {
            'game_id': self.game_id,
            'board': self.board,
            'player_x': self.current_user,
            'player_o': self.opponent,
            'current_player': self.current_player,
            'timestamp': datetime.now().isoformat()
        }
        
        filepath = os.path.join(self.savegame_folder, f"{self.game_id}.json")
        with open(filepath, 'w') as f:
            json.dump(save_data, f, indent=2)
        messagebox.showinfo("Success", f"Game saved with ID: {self.game_id}")
    
    def load_game(self, game_id):
        """Load game state from a JSON file.
        
        Args:
            game_id (str): The game ID to load
            
        Returns:
            bool: True if game loaded successfully, False if file not found
        """
        filepath = os.path.join(self.savegame_folder, f"{game_id}.json")
        
        if not os.path.exists(filepath):
            messagebox.showerror("Error", "Save game not found!")
            return False
        
        with open(filepath, 'r') as f:
            save_data = json.load(f)
        
        self.board = save_data['board']
        self.current_user = save_data['player_x']
        self.opponent = save_data['player_o']
        self.current_player = save_data['current_player']
        self.game_id = game_id
        return True
    
    def end_game(self, winner):
        """Record game result to the database.
        
        Updates user statistics and creates a game record. If there is a winner,
        increments their wins and opponent's losses.
        
        Args:
            winner (str): Username of winner, or None for a tie
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO games (id, player_x, player_o, winner) VALUES (?, ?, ?, ?)',
                      (self.game_id or str(uuid.uuid4()), self.current_user, self.opponent, winner))
        
        if winner:
            cursor.execute('UPDATE users SET wins = wins + 1 WHERE username = ?', (winner,))
            loser = self.opponent if winner == self.current_user else self.current_user
            cursor.execute('UPDATE users SET losses = losses + 1 WHERE username = ?', (loser,))
        
        conn.commit()
        conn.close()
    
    def get_scoreboard(self):
        """Retrieve and return the user scoreboard from database.
        
        Returns:
            list: List of tuples (username, wins, losses) sorted by wins descending
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT username, wins, losses FROM users ORDER BY wins DESC')
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def show_main_menu(self):
        """Display the main menu interface."""
        self.clear_frame()
        self.game_state = GameState.MENU
        
        frame = tk.Frame(self.root)
        frame.pack(pady=20)
        
        title = tk.Label(frame, text="TIC TAC TOE", font=("Arial", 24, "bold"))
        title.pack(pady=10)
        
        btn1 = tk.Button(frame, text="Create Account", width=20, command=self.show_create_account)
        btn1.pack(pady=5)
        
        btn2 = tk.Button(frame, text="Login", width=20, command=self.show_login)
        btn2.pack(pady=5)
        
        btn3 = tk.Button(frame, text="View Scoreboard", width=20, command=self.show_scoreboard)
        btn3.pack(pady=5)
        
        btn4 = tk.Button(frame, text="Exit", width=20, command=self.root.quit)
        btn4.pack(pady=5)
    
    def show_create_account(self):
        """Display create account dialog and process account creation."""
        username = simpledialog.askstring("Create Account", "Enter username:")
        if username is None:
            return
        
        password = simpledialog.askstring("Create Account", "Enter password:", show='*')
        if password is None:
            return
        
        self.create_account(username, password)
        self.show_main_menu()
    
    def show_login(self):
        """Display login dialog and authenticate user."""
        username = simpledialog.askstring("Login", "Enter username:")
        if username is None:
            return
        
        password = simpledialog.askstring("Login", "Enter password:", show='*')
        if password is None:
            return
        
        if self.authenticate_user(username, password):
            self.current_user = username
            self.show_login_menu()
        else:
            messagebox.showerror("Error", "Invalid credentials!")
    
    def show_login_menu(self):
        """Display menu options for logged-in user."""
        self.clear_frame()
        self.game_state = GameState.LOGIN
        
        frame = tk.Frame(self.root)
        frame.pack(pady=20)
        
        title = tk.Label(frame, text=f"Welcome {self.current_user}!", font=("Arial", 18, "bold"))
        title.pack(pady=10)
        
        btn1 = tk.Button(frame, text="Play vs Another User", width=20, command=self.show_opponent_dialog)
        btn1.pack(pady=5)
        
        btn2 = tk.Button(frame, text="Load Saved Game", width=20, command=self.show_load_game_dialog)
        btn2.pack(pady=5)
        
        btn3 = tk.Button(frame, text="Logout", width=20, command=self.show_main_menu)
        btn3.pack(pady=5)
    
    def show_opponent_dialog(self):
        """Display dialog to select and authenticate opponent for a new game."""
        opponent = simpledialog.askstring("Play Game", "Enter opponent username:")
        if opponent is None:
            return
        
        password = simpledialog.askstring("Play Game", f"Enter {opponent}'s password:", show='*')
        if password is None:
            return
        
        if self.authenticate_user(opponent, password):
            self.opponent = opponent
            self.play_game()
        else:
            messagebox.showerror("Error", "Authentication failed!")
    
    def show_scoreboard(self):
        """Display the user scoreboard with win/loss records."""
        self.clear_frame()
        
        frame = tk.Frame(self.root)
        frame.pack(pady=20)
        
        title = tk.Label(frame, text="SCOREBOARD", font=("Arial", 18, "bold"))
        title.pack(pady=10)
        
        scoreboard = self.get_scoreboard()
        for username, wins, losses in scoreboard:
            text = tk.Label(frame, text=f"{username}: {wins}W - {losses}L", font=("Arial", 12))
            text.pack()
        
        btn = tk.Button(self.root, text="Back", command=self.show_main_menu)
        btn.pack(pady=10)

    def show_load_game_dialog(self):
        """Display dialog to load a previously saved game by game ID."""
        game_id = simpledialog.askstring("Load Game", "Enter game ID to load:")
        if game_id is None:
            return
        
        if self.load_game(game_id):
            self.display_game_board()
        else:
            self.show_login_menu()
    
    def play_game(self):
        """Initialize a new game with fresh board state."""
        self.clear_frame()
        self.game_state = GameState.PLAYING
        self.game_id = str(uuid.uuid4())
        self.board = [' '] * 9
        self.current_player = 'X'
        
        self.display_game_board()
    
    def display_game_board(self):
        """Display the interactive game board with clickable buttons."""
        self.clear_frame()
        
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        
        player = self.current_user if self.current_player == 'X' else self.opponent
        title = tk.Label(frame, text=f"{player}'s turn ({self.current_player})", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        board_frame = tk.Frame(frame)
        board_frame.pack(pady=10)
        
        self.buttons = []
        for i in range(9):
            btn = tk.Button(board_frame, text=self.board[i] if self.board[i] != ' ' else '', 
                           font=("Arial", 20), width=5, height=2,
                           command=lambda pos=i: self.on_button_click(pos))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        
        save_btn = tk.Button(button_frame, text="Save Game", command=self.on_save_game)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        quit_btn = tk.Button(button_frame, text="Quit", command=self.show_login_menu)
        quit_btn.pack(side=tk.LEFT, padx=5)
    
    def on_button_click(self, position):
        """Handle board button click events.
        
        Processes move, checks for win/tie conditions, and updates display.
        
        Args:
            position (int): Board position clicked (0-8)
        """
        if self.make_move(position):
            if self.is_winner(self.current_player):
                player = self.current_user if self.current_player == 'X' else self.opponent
                messagebox.showinfo("Game Over", f"{player} wins!")
                self.end_game(player)
                self.show_login_menu()
                return
            
            if self.is_board_full():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.end_game(None)
                self.show_login_menu()
                return
            
            self.switch_player()
            self.display_game_board()
        else:
            messagebox.showwarning("Invalid Move", "Position already taken or invalid!")
    
    def on_save_game(self):
        """Save current game state and return to login menu."""
        self.save_game()
        self.show_login_menu()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()