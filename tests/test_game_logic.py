from logic_utils import check_guess, update_score

def test_winning_guess():
    # Matching value should return a win outcome and confirmation message
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message

def test_guess_too_high():
    # Guess above secret indicates "Too High" outcome and instructs user
    # to lower their next guess (message was backwards in the original code).
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low():
    # Guess below secret indicates "Too Low" outcome and instructs user to
    # raise their next guess.
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_string_secret_does_not_break_comparison():
    # Regression: the original app.py cast the secret to str on even attempts,
    # causing lexicographic ordering ("9" > "50" is True). Passing an int
    # secret must always return the correct directional outcome.
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low", "9 < 50, expected Too Low not Too High"

def test_wrong_guess_never_gains_points():
    # Regression: even-attempt "Too High" guesses previously added +5 to score.
    # Every wrong guess must reduce or leave the score unchanged.
    score_after = update_score(current_score=100, outcome="Too High", attempt_number=2)
    assert score_after < 100, "Score should decrease for a wrong guess"
