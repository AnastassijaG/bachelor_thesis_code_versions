from random import random
# GOOD #
class ConsoleReader:
    # Class for reading user inputs from the console
    @staticmethod
    def read_string(prompt):
        """ Read a string from console with a given prompt """
        return input(prompt)

    @staticmethod
    def read_float(prompt):
        """ Read a float from console with a given prompt """
        while True:
            try:
                return float(ConsoleReader.read_string(prompt))
            except ValueError:
                print("Please enter a valid float value.")

    @staticmethod
    def read_int(prompt):
        """ Read an integer from console with a given prompt """
        while True:
            try:
                return int(ConsoleReader.read_string(prompt))
            except ValueError:
                print("Please enter a valid integer value.")

class Player:
    # Class representing a player in a tennis match
    def __init__(self, probability):
        self.probability = probability
        self.score = 0
        self.games_won = 0
        self.sets_won = 0
        self.matches_won = 0

    def wins_serve(self):
        # Returns a Boolean that is true with probability self.probability
        return random() <= self.probability

    def get_probability(self):
        # Get player's probability to win
        return self.probability

    # Methods for updating player's statistics
    def inc_score(self):
        # Add a point to this player's score
        self.score += 1

    def inc_games_won(self):
        self.games_won += 1

    def inc_sets_won(self):
        self.sets_won += 1

    def inc_matches_won(self):
        self.matches_won += 1

    # Methods for getting player's statistics
    def get_score(self):
        # Returns this player's current game score
        return self.score

    def get_games_won(self):
        return self.games_won

    def get_sets_won(self):
        return self.sets_won

    def get_matches_won(self):
        return self.matches_won

class TennisMatch:
    # Class representing a tennis match
    def __init__(self, probability_a, probability_b):
        self.player_a = Player(probability_a)
        self.player_b = Player(probability_b)
        self.current_server = self.player_a

    # Methods for playing the match
    def play_game(self):
        # Play the game to completion
        y = self.player_a.get_probability()
        while not self.is_over_game():
            self.play_point()

    def play_point(self):
        # Simulate a single point in the game
        if self.current_server.wins_serve():
            self.current_server.inc_score()
        else:
            self.change_server()

    def update_statistic(self, a, b, statistic):
        # Update the specified statistic based on the comparison of scores #
        winner = self.player_a if a > b else self.player_b
        inc_method = f"inc_{statistic}_won"
        getattr(winner, inc_method)()

    def is_over_game(self):
        # Returns True if the game is finished (i.e. one of the players has won).
        a, b = self.get_scores()
        if (a >= 4) or (b >= 4) and abs(a - b) >= 2:
            self.update_statistic(a, b, "games")
            return True
        return False

    # Methods for playing sets and matches
    def play_set(self):
        self.play_game()
        a, b = self.get_games_won()
        while not self.is_over_set():
            self.update_statistic(a, b, "sets")

    def is_over_set(self):
        # Returns true if set is over
        a, b = self.get_sets_won()
        return (a >= 6 or b >= 6) and abs(a - b) >= 2

    def play_match(self):
        self.play_set()
        a, b = self.get_sets_won()
        while not self.is_over_match():
            self.update_statistic(a, b, "matches")

    def is_over_match(self):
        # Returns true if match is over
        a, b = self.get_matches_won()
        return max(a, b) > 3

    # Methods for managing the game state
    def change_server(self):
        # Switch which player is serving
        self.current_server = self.player_a if self.current_server == self.player_b else self.player_b

    def get_scores(self):
        # Returns the current game scores of player A and player B
        return self.player_a.get_score(), self.player_b.get_score()

    def get_games_won(self):
        # Returns the current games won by player A and player B
        return self.player_a.get_games_won(), self.player_b.get_games_won()

    def get_sets_won(self):
        # Returns the current sets won by player A and player B
        return self.player_a.get_sets_won(), self.player_b.get_sets_won()

    def get_matches_won(self):
        # Returns the current matches won by player A and player B
        return self.player_a.get_matches_won(), self.player_b.get_matches_won()

class SimStats:
    # Class for tracking simulation statistics
    def __init__(self):
        self.wins_a = 0
        self.wins_b = 0

    # Update statistics based on the outcome of a match
    def update(self, match):
        a_wins, b_wins = match.get_matches_won()
        if a_wins > b_wins:
            self.wins_a += 1
        else:
            self.wins_b += 1

    # Print a summary report of simulation statistics
    def print_report(self):
        total_matches = self.wins_a + self.wins_b
        print(f"Summary of {total_matches} matches:\n")
        print("         wins (% total)")
        print("---------------------------")
        self.print_line("A", self.wins_a, total_matches)
        self.print_line("B", self.wins_b, total_matches)

    # Helper method for printing a line of the report
    def print_line(self, label, wins, total_matches):
        win_percentage = wins / total_matches * 100 if total_matches else 0
        print(f"Player {label}: {wins:5}    ({win_percentage:.1f}%)")

# Function for printing an introduction to the program
def print_intro():
    print("Program simulates matches of tennis between two")
    print('players called "A" and "B". The ability of each player is')
    print("indicated by a probability (a number between 0 and 1) that")
    print("the player wins the point on the serve.")

# Function for getting user inputs for simulation parameters
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
