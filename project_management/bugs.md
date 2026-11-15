## Bugs Found & Fixed

| Bug | Cause | Fix |
| --- | --- | --- |
| Menu crash on button click (`menu not enabled`) | Button callback disabled menu in `update()`, but loop still called `draw()` | Added `if self.menu.is_enabled():` check before calling `draw()` (`src/menu.py`) |
| Name input stuck on empty string | Checked `name.isalnum()` when name was empty (`"".isalnum()` is `False`) | Check incoming key `event.unicode.isalnum()` instead of the whole string (`src/highscores.py`) |
| Menu only navigated by arrow keys | `pygame-menu` default bindings | Added custom handlers for `K_w`, `K_s`, and `K_SPACE` (`src/menu.py`) |
| Ghosts not respawning at corner after being eaten | Ghost stayed at collision position instead of returning to spawn | Reset ghost position back to its corner upon being eaten (`src/ghosts.py`) |
| Ghosts standing still | Chasing algorithm got stuck when preferred direction was blocked | Improved chase/movement algorithm so ghosts always select a valid open corridor (`src/ghosts.py`) |
| `max_time` & `points_per_ghost` not accessible | Values from `config.json` were not passed into `DrawMaze.__init__()` | Added them to `DrawMaze` constructor and passed them from `GameManager` (`src/drawmaze.py`, `src/game_manager.py`) |
| `Makefile lint` didn't run `mypy` | `flake8` exited with error code on lint issues, stopping execution before `mypy` | Updated Makefile lint target so both tools execute (`Makefile`) |
| Cheat mode couldn't be turned off | Once cheat mode was activated, there was no way to toggle it off | Added return key (`x`) to exit cheat mode (`src/player_mechanics.py`, `src/drawmaze.py`) |
| Spaces-only names accepted in highscores | No check for whitespace-only strings | Added `name.strip()` check on submit to reject empty/spaces input (`src/highscores.py`) |
| Pac-Man spawns inside wall | Even maze sizes $\ge 14\times 10$ have "42" pattern with cell `15` at center | Added `_find_spawn_cell()` to shift spawn left until finding open cell (`src/drawmaze.py`) |
| `DrawMaze` return type mismatch | Returned `(action, score)` on quit, but `Results` dataclass on win/lose | Standardized all exits to return `Results(outcome, score, lives)` (`src/drawmaze.py`) |
