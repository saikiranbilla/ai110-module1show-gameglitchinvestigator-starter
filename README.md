# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game purpose:** A number-guessing game where the player tries to identify a hidden secret number within a limited number of attempts. The difficulty setting changes the number range and attempt limit.

**Bugs found:**
1. `st.session_state.attempts` was initialized to `1` instead of `0`, causing an off-by-one in the "Attempts left" display and triggering the string-cast bug on the very first guess.
2. On every even-numbered attempt, the secret was cast to a `str` before comparison. Python string ordering made `"9" > "50"` evaluate to `True`, so a guess of 9 against secret 50 incorrectly said "Too High".
3. The hints ("Go HIGHER!" / "Go LOWER!") were reversed — the logic returned the opposite direction.
4. Incorrect guesses with outcome "Too High" on even attempts *added* +5 to the score instead of deducting points.
5. The "New Game" button regenerated the secret using the hardcoded range `1–100` regardless of the chosen difficulty.

**Fixes applied:**
- `app.py`: Changed attempts initialization from `1` to `0`.
- `app.py`: Removed the conditional `str()` cast so the secret is always passed as `int` to `check_guess`.
- `app.py`: Fixed the new-game secret to use `random.randint(low, high)` (difficulty-aware range).
- `logic_utils.py`: Removed the even-attempt `+5` branch in `update_score`; wrong guesses always deduct 5.
- `logic_utils.py`: The reversed hint directions were already corrected in the refactored version.
- `tests/test_game_logic.py`: Added two regression tests — one for the string-comparison bug and one for the score-reward bug. All 5 tests pass with `pytest`.

## 📸 Demo

_Run `python -m streamlit run app.py`, open the Developer Debug Info expander to see the secret, and make a winning guess to confirm balloons appear and the final score is displayed._

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
