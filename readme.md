# Chess AI Game

A Python-based chess game built with **pygame** for the GUI and **python-chess** for chess logic.
The game supports four player types:

* **Human** – Player makes moves manually via the GUI.
* **AI** – Uses a Minimax search algorithm with a heuristic evaluation.
* **Optimized AI** – Minimax with move ordering for improved search efficiency.
* **Random** – Selects legal moves randomly.

---

## Features

* **Graphical Interface** built with pygame.
* **Legal move validation** via python-chess.
* Multiple **player type configurations** (e.g., Human vs AI, AI vs AI, Random vs Human, etc.).
* **AI Agent**: Implements Minimax (with alpha-beta pruning) search.
* **Optimized AI Agent**: Same as AI but with move ordering to improve search performance.
* **Random Agent**: Plays completely random legal moves.
* Detects **checkmate**, **stalemate**, and other game-ending conditions.

---

## Requirements

Install dependencies with:

```bash
pip install pygame python-chess
```

---

## Usage

Run the game:

```bash
python main.py
```

Choose the player types from the start menu.

---

## AI Implementation

* **Minimax Algorithm**: Evaluates future board states up to a set depth.
* **Move Ordering (Optimized AI)**: Orders moves to search more promising ones first, improving pruning efficiency.


---

## Credits

* **python-chess** for chess logic and rules enforcement.
* **pygame** for rendering the game interface.

---
