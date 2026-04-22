<a id="TicTacToe"></a>

# TicTacToe

<a id="TicTacToe.GameState"></a>

## GameState Objects

```python
class GameState(Enum)
```

Enumeration for different game states.

**Attributes**:

- `MENU` - Main menu state
- `LOGIN` - Login/post-login state
- `PLAYING` - Active game state
- `GAME_OVER` - Game finished state

<a id="TicTacToe.TicTacToe"></a>

## TicTacToe Objects

```python
class TicTacToe()
```

A Tic Tac Toe game application with user authentication and game persistence.

This class implements a GUI-based Tic Tac Toe game using tkinter with SQLite
database backend for user management and game history tracking. Players can
create accounts, authenticate, play against each other, and save/load games.

**Attributes**:

- `root` _tk.Tk_ - The root tkinter window
- `db_path` _str_ - Path to the SQLite database file
- `savegame_folder` _str_ - Directory for saving game states
- `current_user` _str_ - Currently logged-in username
- `opponent` _str_ - Current opponent username
- `board` _list_ - 9-element list representing the game board
- `current_player` _str_ - 'X' or 'O' representing whose turn it is
- `game_state` _GameState_ - Current state of the game
- `game_id` _str_ - Unique identifier for current game
- `buttons` _list_ - List of tkinter button widgets for the board

<a id="TicTacToe.TicTacToe.__init__"></a>

#### \_\_init\_\_

```python
def __init__(root)
```

Initialize the Tic Tac Toe application.

**Arguments**:

- `root` _tk.Tk_ - The root tkinter window

<a id="TicTacToe.TicTacToe.clear_frame"></a>

#### clear\_frame

```python
def clear_frame()
```

Clear all widgets from the root window.

<a id="TicTacToe.TicTacToe.create_account"></a>

#### create\_account

```python
def create_account(username, password)
```

Create a new user account in the database.

**Arguments**:

- `username` _str_ - Desired username
- `password` _str_ - Desired password (will be hashed)
  

**Returns**:

- `bool` - True if account created successfully, False if username exists

<a id="TicTacToe.TicTacToe.authenticate_user"></a>

#### authenticate\_user

```python
def authenticate_user(username, password)
```

Authenticate user credentials against database.

**Arguments**:

- `username` _str_ - Username to authenticate
- `password` _str_ - Password to verify
  

**Returns**:

- `bool` - True if credentials are valid, False otherwise

<a id="TicTacToe.TicTacToe.is_winner"></a>

#### is\_winner

```python
def is_winner(player)
```

Check if a player has won the game.

**Arguments**:

- `player` _str_ - 'X' or 'O'
  

**Returns**:

- `bool` - True if player has three in a row, False otherwise

<a id="TicTacToe.TicTacToe.is_board_full"></a>

#### is\_board\_full

```python
def is_board_full()
```

Check if the game board is completely filled.

**Returns**:

- `bool` - True if no empty spaces remain, False otherwise

<a id="TicTacToe.TicTacToe.make_move"></a>

#### make\_move

```python
def make_move(position)
```

Make a move at the specified board position.

**Arguments**:

- `position` _int_ - Board position (0-8)
  

**Returns**:

- `bool` - True if move was valid and made, False otherwise

<a id="TicTacToe.TicTacToe.switch_player"></a>

#### switch\_player

```python
def switch_player()
```

Switch current player between 'X' and 'O'.

<a id="TicTacToe.TicTacToe.save_game"></a>

#### save\_game

```python
def save_game()
```

Save current game state to a JSON file.

Creates a JSON file in the savegames folder with board state, player info,
and timestamp. Displays success message with game ID.

<a id="TicTacToe.TicTacToe.load_game"></a>

#### load\_game

```python
def load_game(game_id)
```

Load game state from a JSON file.

**Arguments**:

- `game_id` _str_ - The game ID to load
  

**Returns**:

- `bool` - True if game loaded successfully, False if file not found

<a id="TicTacToe.TicTacToe.end_game"></a>

#### end\_game

```python
def end_game(winner)
```

Record game result to the database.

Updates user statistics and creates a game record. If there is a winner,
increments their wins and opponent's losses.

**Arguments**:

- `winner` _str_ - Username of winner, or None for a tie

<a id="TicTacToe.TicTacToe.get_scoreboard"></a>

#### get\_scoreboard

```python
def get_scoreboard()
```

Retrieve and return the user scoreboard from database.

**Returns**:

- `list` - List of tuples (username, wins, losses) sorted by wins descending

<a id="TicTacToe.TicTacToe.show_main_menu"></a>

#### show\_main\_menu

```python
def show_main_menu()
```

Display the main menu interface.

<a id="TicTacToe.TicTacToe.show_create_account"></a>

#### show\_create\_account

```python
def show_create_account()
```

Display create account dialog and process account creation.

<a id="TicTacToe.TicTacToe.show_login"></a>

#### show\_login

```python
def show_login()
```

Display login dialog and authenticate user.

<a id="TicTacToe.TicTacToe.show_login_menu"></a>

#### show\_login\_menu

```python
def show_login_menu()
```

Display menu options for logged-in user.

<a id="TicTacToe.TicTacToe.show_opponent_dialog"></a>

#### show\_opponent\_dialog

```python
def show_opponent_dialog()
```

Display dialog to select and authenticate opponent for a new game.

<a id="TicTacToe.TicTacToe.show_scoreboard"></a>

#### show\_scoreboard

```python
def show_scoreboard()
```

Display the user scoreboard with win/loss records.

<a id="TicTacToe.TicTacToe.show_load_game_dialog"></a>

#### show\_load\_game\_dialog

```python
def show_load_game_dialog()
```

Display dialog to load a previously saved game by game ID.

<a id="TicTacToe.TicTacToe.play_game"></a>

#### play\_game

```python
def play_game()
```

Initialize a new game with fresh board state.

<a id="TicTacToe.TicTacToe.display_game_board"></a>

#### display\_game\_board

```python
def display_game_board()
```

Display the interactive game board with clickable buttons.

<a id="TicTacToe.TicTacToe.on_button_click"></a>

#### on\_button\_click

```python
def on_button_click(position)
```

Handle board button click events.

Processes move, checks for win/tie conditions, and updates display.

**Arguments**:

- `position` _int_ - Board position clicked (0-8)

<a id="TicTacToe.TicTacToe.on_save_game"></a>

#### on\_save\_game

```python
def on_save_game()
```

Save current game state and return to login menu.

