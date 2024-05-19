from random import random

# GOOD CODE #
class TennisMatch:
    def __init__(self, prob_a, prob_b):
        self.prob_a = prob_a
        self.prob_b = prob_b
        self.score_a = 0
        self.score_b = 0
        self.games_a = 0
        self.games_b = 0
        self.sets_a = 0
        self.sets_b = 0
        self.matches_a = 0
        self.matches_b = 0

    def play_match(self):
        while not self.is_over_match():
            self.play_set()

    def play_set(self):
        while not self.is_over_set():
            self.play_game()

    def play_game(self):
        while not self.is_over_game():
            if random() < self.prob_a:
                self.score_a += 1
            else:
                self.score_b += 1
        self.update_scores()
        self.score_a = 0
        self.score_b = 0

    def is_over_game(self):
        if abs(self.score_a - self.score_b) >= 2 and (self.score_a >= 4 or self.score_b >= 4):
            return True
        return False

    def is_over_set(self):
        if (self.games_a >= 6 or self.games_b >= 6) and abs(self.games_a - self.games_b) >= 2:
            return True
        return False

    def is_over_match(self):
        if self.sets_a >= 3 or self.sets_b >= 3:
            return True
        return False

    def get_winner(self):
        if self.sets_a > self.sets_b:
            return 'A'
        elif self.sets_b > self.sets_a:
            return 'B'
        elif self.matches_a > self.matches_b:
            return 'A'
        elif self.matches_b > self.matches_a:
            return 'B'
        return None

    def update_scores(self):
        if self.score_a > self.score_b:
            self.games_a += 1
        else:
            self.games_b += 1
        self.update_sets()

    def update_sets(self):
        if self.games_a > self.games_b:
            self.sets_a += 1
        else:
            self.sets_b += 1
        self.update_matches()

    def update_matches(self):
        if self.sets_a > self.sets_b:
            self.matches_a += 1
        else:
            self.matches_b += 1

def main():
    print("This program simulates tennis matches between two players, A and B.")
    prob_a = float(input("Enter the probability of player A winning a point (0-1): "))
    prob_b = float(input("Enter the probability of player B winning a point (0-1): "))
    num_matches = int(input("How many matches to simulate? "))

    wins_a = 0
    wins_b = 0

    for _ in range(num_matches):
        match = TennisMatch(prob_a, prob_b)
        match.play_match()
        winner = match.get_winner()
        if winner == 'A':
            wins_a += 1
        elif winner == 'B':
            wins_b += 1

    total_matches = wins_a + wins_b
    print(f"\nSummary of {total_matches} matches:")
    print(f"Player A wins: {wins_a} ({(wins_a / total_matches) * 100:.2f}%)")
    print(f"Player B wins: {wins_b} ({(wins_b / total_matches) * 100:.2f}%)")

if __name__ == "__main__":
    main()
