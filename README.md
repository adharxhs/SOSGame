# SOS Game

A Python-based implementation of the classic **SOS board game** with a graphical interface built using Tkinter. Supports multiplayer (2–4 players) and single-player vs AI modes.

---

## Table of Contents

- [About the Game](#about-the-game)
- [Project Structure](#project-structure)
- [File Breakdown](#file-breakdown)
  - [board.py](#boardpy)
  - [engine.py](#enginepy)
  - [bot.py](#botpy)
  - [gui.py](#guipy)
  - [main.py](#mainpy)
- [How to Play](#how-to-play)
- [Running the Game](#running-the-game)
  - [Method 1: Running from Source](#method-1-running-from-source)
  - [Method 2: Running the Prebuilt Executable](#method-2-running-the-prebuilt-executable)
- [Game Rules](#game-rules)
- [AI Behaviour](#ai-behaviour)
- [Architecture Overview](#architecture-overview)

---

## About the Game

SOS is a strategy board game where players take turns placing either the letter **S** or **O** on a grid. The goal is to form the sequence **S-O-S** in any direction (horizontal, vertical, or diagonal). Each completed SOS sequence earns the player a point, and they get an extra turn. The player with the most SOS sequences when the board is full wins.

---

## Project Structure

```
sos/
└── src/
    ├── board.py       # Board data structure and game logic
    ├── engine.py      # Game state management layer
    ├── bot.py         # AI opponent logic
    ├── gui.py         # Tkinter GUI (setup screen + game screen)
    ├── main.py        # Entry point
    └── icon.png       # Application icon(png)
    └── icon.ico       # Application icon(ico)

```

---

## File Breakdown

### `board.py`

The foundational data layer. Manages the raw board state and all cell-level operations.

**Responsibilities:**
- Initialises an N×N grid populated with empty cells (`-`)
- Validates index bounds (`validIndexCheck`) and symbol validity (`validSymbolCheck`)
- Handles cell insertion (`insert`) and removal (`remove`)
- Detects SOS matches around a given cell (`checkForMatches`) — checks all 8 directions for both `S` (endpoint) and `O` (middle) placements
- Reports whether the board is full (`isFull`)

**Key class:** `Board(maxboardsize)`

---

### `engine.py`

The game state and turn management layer. Acts as the intermediary between the GUI and the board/bot layers.

**Responsibilities:**
- Manages player turn order (`currentplayer`, `updateCurrentPlayer`)
- Tracks live scores (`playerScores`) and finalised scores for quit players (`finalScores`)
- Delegates move execution to `Board` and score counting to `checkForMatches`
- Supports move undo via `cancelMove`
- Instantiates and queries the `Bot` when single-player mode is active
- Exposes clean getter methods for the GUI (`getBoardCell`, `getCurrentPlayer`, `getPlayerScores`, etc.)

**Key class:** `GameEngine(boardsize, playerCount, mode)`

---

### `bot.py`

The AI opponent. Implements a priority-tiered heuristic strategy — no minimax, but effective for casual play.

**Move priority (highest to lowest):**

| Tier | Method | Description |
|------|--------|-------------|
| 1 | `tryScore()` | Scans the entire board for any move that immediately completes an SOS |
| 2 | `tryBlock(lastMove)` | Checks cells near the opponent's last move for any threat to block |
| 3 | `trySetup()` | Places an `S` on the cell with the most adjacent `S`/`O` neighbours to maximise future scoring potential |
| 4 | `fallback()` | Places `S` on a random empty cell as a last resort |

**Key class:** `Bot(board)`

---

### `gui.py`

The complete graphical interface built with Tkinter. Manages both the setup screen and the active game screen.

**Responsibilities:**
- **Setup screen:** Allows selecting game mode (Multiplayer / vs AI), number of players (2–4), and grid size (4×4 to 8×8)
- **Game screen:** Renders the board as a grid of buttons, handles click events, displays live scores and current player
- Manages the `active_players` set to support mid-game player quitting
- Schedules bot moves asynchronously using `root.after()` to avoid blocking the UI thread
- `bot_active` flag prevents human input during the bot's turn
- `resource_path()` helper resolves asset paths correctly for both script execution and PyInstaller-packaged executables

**Key class:** `SOSGameGUI(root)`

---

### `main.py`

The application entry point. Initialises the Tkinter root window, sets the app icon, and launches the GUI.


---

## How to Play

1. **Launch the game** using either method described further below.
2. On the **setup screen**, select:
   - **Game Mode:** Multiplayer (local) or vs AI
   - **Number of Players:** 2, 3, or 4 (Multiplayer only; vs AI is always 2-player)
   - **Grid Size:** 4×4, 5×5, 6×6, or 8×8
3. Click **START GAME**.
4. On your turn, choose **S** or **O** from the symbol selector on the right panel.
5. Click any empty cell on the board to place your symbol.
6. If you complete an **SOS** sequence, you score a point and **take another turn**.
7. Use **Quit Game** to forfeit your position mid-game (other players continue).
8. When the board is full, scores are tallied and the winner is announced.

---

## Running the Game

### Method 1: Running from Source

**Requirements:**
- Python 3.8 or higher
- Tkinter (included in standard Python distributions; on Linux install `python3-tk` if missing)

**Steps:**

```bash
# Clone or download the project
cd sos/src

# Run directly
python main.py
```

> On Linux, if Tkinter is not available:
> ```bash
> # Fedora/RHEL
> sudo dnf install python3-tkinter
>
> # Debian/Ubuntu
> sudo apt install python3-tk
> ```

---

### Method 2: Running the Prebuilt Executable

A prebuilt standalone executable is provided in the `dist/` directory (Windows) and as a binary in the project root (Linux). No Python installation is required.

**On Windows:**

```
dist\SOS.exe
```

Double-click `SOS.exe` in File Explorer, or run from terminal:

```cmd
.\dist\SOS.exe
```

**On Linux:**

The `SOS` binary (ELF executable) is located in the project root:

```bash
# Make executable if needed
chmod +x ./SOS

# Run
./SOS
```

> Both executables are packaged with PyInstaller and include all dependencies (`icon.png`, source modules) bundled internally. No external files need to be present alongside the binary.

---

## Game Rules

- The board is an N×N grid (configurable: 4 to 8).
- Players alternate turns placing **S** or **O** in any empty cell.
- A completed **S-O-S** sequence in any of the 8 directions scores **1 point**.
- A single move can score **multiple points** simultaneously if it completes multiple sequences.
- A player who scores **gets an additional turn** immediately.
- The game ends when the board is completely filled.
- The player with the **highest score** wins.
- In multiplayer mode, players may **quit mid-game**; the remaining players continue. If only one player remains, they are declared the winner.

---

## AI Behaviour

The bot (Player 2 in vs AI mode) uses a greedy heuristic with four priority tiers:

1. **Score immediately** — always takes a scoring move if one exists.
2. **Block threats** — responds to opponent moves by checking nearby cells for danger.
3. **Setup positioning** — favours cells with more adjacent letters to build future opportunities.
4. **Random fallback** — picks any available empty cell if no strategic option is found.

The bot is not exhaustive (no minimax/alpha-beta pruning), so it can be outplayed with deliberate setups. This keeps it accessible while still providing a reasonable challenge.

---

## Architecture Overview

```
main.py
  └── gui.py  (SOSGameGUI)
        └── engine.py  (GameEngine)
              ├── board.py  (Board)
              └── bot.py    (Bot)  ← only in single-player mode
```

The three-layer architecture cleanly separates concerns:

| Layer | Module | Responsibility |
|-------|--------|----------------|
| **Data** | `board.py` | Raw grid state, match detection, validity checks |
| **Logic** | `engine.py` | Turn management, scoring, player state |
| **Presentation** | `gui.py` | Rendering, user input, async bot scheduling |

`bot.py` operates as an auxiliary strategy module, accessed exclusively through `engine.py`.
