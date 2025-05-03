from itertools import product
from belief_base import BeliefBase
from parser import parse_formula
import random

# Define colors and positions
COLORS = ['R', 'G', 'B', 'Y', 'O', 'P']
CODE_LENGTH = 4

def encode_code_as_formula(code):
    terms = [f"P{i+1}_{color}" for i, color in enumerate(code)]
    return parse_formula(" & ".join(terms))

def get_feedback(guess, secret):
    black = sum(g == s for g, s in zip(guess, secret))
    guess_counts = {c: guess.count(c) for c in set(guess)}
    secret_counts = {c: secret.count(c) for c in set(secret)}
    total_matches = sum(min(guess_counts.get(c, 0), secret_counts.get(c, 0)) for c in COLORS)
    white = total_matches - black
    return black, white

def is_feedback_match(guess, candidate, expected_feedback):
    return get_feedback(guess, candidate) == expected_feedback

def code_to_str(code):
    return ''.join(code)

def run_mastermind_with_belief_base():
    all_codes = list(product(COLORS, repeat=CODE_LENGTH))
    secret_code = random.choice(all_codes)   # for deterministic result

    bb = BeliefBase()
    for code in all_codes:
        formula = encode_code_as_formula(code)
        bb.expand(formula, source='init')

    current_beliefs = all_codes.copy()
    guess = current_beliefs[0]
    attempts = 0

    print("Secret code is:", code_to_str(secret_code))

    while True:
        feedback = get_feedback(guess, secret_code)
        attempts += 1
        print(f"Guess {attempts}: {code_to_str(guess)} | Feedback: {feedback}")

        if feedback[0] == CODE_LENGTH:
            print(f"Code broken in {attempts} attempts!")
            break

        valid_codes = [c for c in current_beliefs if is_feedback_match(guess, c, feedback)]
        current_beliefs = valid_codes

        bb = BeliefBase()
        for code in current_beliefs:
            formula = encode_code_as_formula(code)
            bb.expand(formula, source='feedback_filter')

        guess = current_beliefs[0]

if __name__ == "__main__":
    run_mastermind_with_belief_base()
