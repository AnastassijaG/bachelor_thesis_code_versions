from random import random
# BAD (изначально был good)#
class ConsoleReader:
    @staticmethod
    def read_string(prompt):
        return input(prompt)

    @staticmethod
    def read_float(prompt):
        while True:
            try:
                return float(ConsoleReader.read_string(prompt))
            except ValueError:
                print("Please enter a valid float value.")

    @staticmethod
    def read_int(prompt):
        while True:
            try:
                return int(ConsoleReader.read_string(prompt))
            except ValueError:
                print("Please enter a valid integer value.")

class Player:
    def __init__(self, probability):
        self.probability = probability
        self.score = 0
        self.games_won = 0
        self.sets_won = 0
        self.matches_won = 0

    def wins_serve(self):
        return random() <= self.probability

class TennisMatch:
    def __init__(self, probability_a, probability_b):
        self.player_a = Player(probability_a)
        self.player_b = Player(probability_b)
        self.server = self.player_a

    def play_game(self):
        while not self.is_game_over():
            if self.player_a.wins_serve():
                self.player_a.score += 1
            else:
                self.player_b.score += 1

    def is_game_over(self):
        a_score, b_score = self.player_a.score, self.player_b.score
        if (a_score >= 4) or (b_score >= 4):
            if abs(a_score - b_score) >= 2:
                if a_score > b_score:
                    self.player_a.games_won += 1
                else:
                    self.player_b.games_won += 1
                return True
            else:
                return False
        else:
            return False

    def play_set(self):
        self.play_game()
        while not self.is_set_over():
            if self.player_a.games_won > self.player_b.games_won:
                self.player_a.sets_won += 1
            else:
                self.player_b.sets_won += 1

    def is_set_over(self):
        a_sets_won, b_sets_won = self.player_a.sets_won, self.player_b.sets_won
        if a_sets_won == 7 or b_sets_won == 7:
            return True
        elif a_sets_won >= 6 or b_sets_won >= 6:
            if abs(a_sets_won - b_sets_won) >= 2:
                return True
            else:
                return False
        else:
            return False

    def play_match(self):
        self.play_set()
        while not self.is_match_over():
            if self.player_a.sets_won > self.player_b.sets_won:
                self.player_a.matches_won += 1
            else:
                self.player_b.matches_won += 1

    def is_match_over(self):
        if self.player_a.matches_won > 3 or self.player_b.matches_won > 3:
            return True
        else:
            return False

    def change_server(self):
        if self.server == self.player_a:
            self.server = self.player_b
        else:
            self.server = self.player_a

class SimStats:
    def __init__(self):
        self.wins_a = 0
        self.wins_b = 0

    def update(self, match):
        if match.player_a.matches_won > match.player_b.matches_won:
            self.wins_a += 1
        else:
            self.wins_b += 1

    def print_report(self):
        total_matches = self.wins_a + self.wins_b
        print(f"Summary of {total_matches} matches:\n")
        print("         wins (% total)")
        print("---------------------------")
        self.print_line("A", self.wins_a, total_matches)
        self.print_line("B", self.wins_b, total_matches)

    def print_line(self, label, wins, total_matches):
        win_percentage = wins / total_matches * 100 if total_matches else 0
        print(f"Player {label}: {wins:5}    ({win_percentage:.1f}%)")

def print_intro():
    print("This program simulates matches of tennis between two")
    print('players called "A" and "B". The ability of each player is')
    print("indicated by a probability (a number between 0 and 1) that")
    print("the player wins the point on the serve.")


def get_inputs():
    # Returns the three simulation parameters
    a = None
    b = None
    n = None
    while (a == None) or (b == None) or (n == None):
        a = ConsoleReader.read_float("What is the prob. player A? ")
        b = ConsoleReader.read_float("What is the prob. player B? ")
        n = ConsoleReader.read_int("How many matches? ")
    return a, b, n


def main():
    print_intro()
    prob_a, prob_b, num_matches = get_inputs()
    stats = SimStats()
    for _ in range(num_matches):
        game = TennisMatch(prob_a, prob_b)
        game.play_match()
        stats.update(game)
    stats.print_report()

if __name__ == "__main__":
    main()
input("\nPress <Enter> to quit")