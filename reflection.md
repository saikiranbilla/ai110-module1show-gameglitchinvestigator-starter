# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, it looked functional on the surface — there was a guess input, a submit button, difficulty settings, and a developer debug panel. However, several things were immediately wrong. First, the "Attempts left" counter was already off by one before I even guessed, because `st.session_state.attempts` started at `1` instead of `0`, so the display read one less attempt than it should. Second, the hints were backwards: guessing higher than the secret would say "Go HIGHER!" and guessing lower would say "Go LOWER!" — the exact opposite of correct. Third, on every even-numbered attempt, the secret number was silently cast to a string before being passed to `check_guess`, which caused Python to use lexicographic (alphabetical) ordering — meaning a guess of `9` against a secret of `50` would say "Too High" because the string `"9"` sorts after `"50"`. A fourth, subtler bug rewarded the player with +5 score points for a wrong "Too High" guess on even attempts, so your score could actually go *up* even when you were wrong.

---

## 2. How did you use AI as a teammate?

I used Claude Code (Anthropic's AI CLI) as my primary AI assistant throughout this project. For a correct suggestion, I asked Claude to trace why the secret was being converted to a string on alternate guesses; it correctly identified lines 105–110 in `app.py` where `secret = str(st.session_state.secret)` was conditional on `attempts % 2 == 0`, and explained that this would flip outcomes for single-digit guesses due to lexicographic string ordering. I verified this by manually testing `check_guess(9, "50")` in a Python REPL and confirming `"9" > "50"` returns `True`. For a misleading suggestion, the AI initially proposed wrapping all comparisons in `try/except TypeError` inside `check_guess` as the fix — that approach would have masked the real bug rather than removing the broken string-conversion entirely; I rejected it, removed the string cast in `app.py` instead, and confirmed the TypeError path in `logic_utils.py` was no longer reachable.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed only when both a manual play-through and at least one pytest case confirmed the correct behavior. For the string-comparison bug I added `test_string_secret_does_not_break_comparison`: it calls `check_guess(9, 50)` and asserts the outcome is `"Too Low"` — before the fix this test failed because the old code would have returned `"Too High"`. For the score bug I added `test_wrong_guess_never_gains_points`: it calls `update_score(100, "Too High", attempt_number=2)` and asserts the result is less than 100; this also failed against the original code because even-attempt wrong guesses returned `current_score + 5`. Running `pytest -v` showed all 5 tests passing after both fixes were applied, giving me high confidence the regressions were closed. Claude helped me phrase the assertions clearly and suggested using a named `attempt_number=2` keyword argument to make the even-attempt trigger obvious to anyone reading the test.

---

## 4. What did you learn about Streamlit and state?

The secret number kept changing in the original app because Streamlit re-runs the entire Python script from top to bottom every time the user interacts with a widget (clicking Submit, for example). Without `st.session_state`, the line `random.randint(low, high)` would execute again on every rerun, picking a brand new secret each click. Session state is like a persistent dictionary that survives across reruns in the same browser session — you store a value in it once (using an `if "key" not in st.session_state` guard) and it stays put. Think of Streamlit reruns like refreshing a webpage: everything you put in a regular Python variable disappears on each refresh, but `st.session_state` is like the browser's `localStorage` — it remembers what you stored last time. The fix that gave the game a stable secret was the `if "secret" not in st.session_state` guard on line 39 of `app.py`, which ensures the secret is only generated once per session.

---

## 5. Looking ahead: your developer habits

The habit I most want to reuse is writing a failing test *before* applying the fix — the red-then-green cycle makes it obvious when a bug is truly closed versus just silently passing. One thing I would do differently next time is start AI conversations with a more constrained prompt: instead of "how do I fix this file?", ask "explain only what this specific line does" first, because narrow questions get sharper answers and stop the AI from proposing sweeping refactors that introduce new issues. This project changed how I think about AI-generated code by making it concrete: AI can produce code that looks correct, passes a quick read, and still contains subtle logic errors (like the string-cast trick) that only surface under specific runtime conditions — so treating AI output as a first draft that requires test-driven verification, not a finished product, is the right default.
