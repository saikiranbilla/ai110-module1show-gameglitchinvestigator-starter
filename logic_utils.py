def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # based on original implementation from app.py
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    # default to normal range if unrecognized
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low".
    The helper also returns a user-facing hint message; note that the
    original implementation in app.py had the directions reversed, so this
    version fixes that bug.
    """
    # match the logic that app.py used but correct the wording
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            # guess is too high -> tell user to go lower
            return "Too High", "📉 Go LOWER!"
        else:
            # guess is too low -> tell user to go higher
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        # in the original code they stringified the guess for some reason
        # when comparing with a secret stored as str; replicate that logic
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIXME was here: even-numbered "Too High" attempts rewarded +5 points.
    # Wrong guesses should never increase the score.
    # FIX: always deduct 5 for any wrong guess. Identified with Claude Code.
    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
