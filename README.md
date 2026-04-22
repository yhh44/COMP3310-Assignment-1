
# TicTacDoh

TicTacDoh is a Tic Tac Toe game built in Python. This project is designed as an educational exercise where students identify security vulnerabilities and recommend fixes. For full instructions on what is needed for the assignment, please refer to the assignment specification in iLearn

## Getting Started

### Prerequisites
- Python 3.8 or higher
- python-tk (for the GUI)

### Installing python-tk

**macOS:**
```bash
brew install python-tk@3.9
```
Note: check what version of python you have installed and adjust the command accordingly, e.g. if you have python 3.10 then you may need to run "brew install python-tk@3.10" instead.

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Windows:**
tkinter comes bundled with Python. If missing, reinstall Python and ensure "tcl/tk and IDLE" is selected during installation.

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd TicTacDohLocal
```

2. Create a virtual environment:
```bash
python -m venv venv
OR
python3 -m venv venv
```

3. Activate the virtual environment:
- **macOS/Linux:**
```bash
source venv/bin/activate
```
- **Windows:**
```bash
venv\Scripts\activate
OR it could be
.\venv\bin\Activate.ps1
```
Note for windows users: if you get some red letters saying "...because running scripts is disabled ..." then you may want to run this command in PowerShell as administrator and then rerun the above command to activate the virtual environment:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

4. Install dependencies needed to run the game:
```bash
pip install -r requirements.txt
```

## Running the Game inside the virtual environment

```bash
python tictactoe.py
```

## Closing off your python environment
When you've finished working with the project and want to get back to regular command line operations, type in the following command in your (venv) prompt to return to the normal command line / PowerShell / terminal prompt:
```bash
deactivate
```

## Project Goals

This project intentionally contains security vulnerabilities. Students should:
- Identify potential security issues
- Document findings
- Provide recommendations for improvements


