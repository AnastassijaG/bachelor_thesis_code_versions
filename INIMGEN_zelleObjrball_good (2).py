from random import random
# GOOD #
class Player:
    # A Player keeps track of his probability
    def __init__(self, probability):
        # Initialize a player with the given probability of winning a serve
        self.probability = probability

    def get_probability(self):
        # Returns this player's probability
        return self.probability

class PlayerStatistics:
    def __init__(self):
        # Initialize player statistics
        self.score = 0

    def increment_score(self):
        # Increment player's score by 1
        self.score += 1

    def get_score(self):
        # Returns this player's current score
        return self.score

class RBallGame:
    # A RBallGame represents a game in progress. A game has two players
    # and keeps track of which one is currently serving
    def __init__(self, probA, probB):
        # Initialize a game with two players and their respective probabilities
        self.players = [Player(probA), Player(probB)]
        self.server_index = 0
        # Initialize two players statistics
        self.player_stats = [PlayerStatistics() for _ in range(2)]

    def play(self):
        # Play the game to until it is over
        while not self.is_over():
            self.play_point()

    def play_point(self):
        # Simulate a single point in the game
        self.player_stats[self.server_index].increment_score() if self.server_wins_serve() else self.change_server()

    def server_wins_serve(self):
        # Determine if the server wins the serve
        return random() <= self.players[self.server_index].get_probability()

    def is_over(self):
        # Returns game is finished (i.e. one of the players has won).
        scores = self.get_scores()
        return any(score == 15 or (scores[1 - i] == 0 and score == 7) for i, score in enumerate(scores))

    def change_server(self):
        # Switch which player is serving
        self.server_index = 1 - self.server_index

    def get_scores(self):
        # Returns the current scores of all players
        return [player_stat.get_score() for player_stat in self.player_stats]

class SimStats:
    # SimStats handles accumulation of statistics across multiple
    #   (completed) games. This version tracks the wins and shutouts for
    #   each player.
    def __init__(self):
        # Initialize statistics for wins and shutouts
        self.wins = [0, 0]
        self.shuts = [0, 0]

    def update(self, game):
        # Update statistics based on the outcome of a game
        scores = game.get_scores()
        winner_index = scores.index(max(scores))
        # Player wins
        self.wins[winner_index] += 1
        # Check if opponent has been shut out
        if scores[1 - winner_index] == 0:
            self.shuts[winner_index] += 1

    def print_report(self, n):
        # Print a report of the simulation results
        print("Summary of", n, "games:\n")
        print("         wins (% total)  shutouts (% wins)   ")
        print("----------------------------------------")
        for label, wins, shuts in zip("AB", self.wins, self.shuts):
            # Print a line of the report for a player
            shut_str = "-----" if wins == 0 else "{0:4.1%}".format(shuts / wins)
            print(f"Player {label}:{wins:5}    ({wins / n:5.1%})  {shuts:11}  ({shut_str})")

def print_intro():
    print("This program simulates games of racquetball between two players called 'A' and 'B'.")
    print("The ability of each player is indicated by a probability (a number between 0 and 1)")
    print("that the player wins the point when serving. Player A always has the first serve.\n")

def get_inputs():
    # Returns the three simulation parameters
    a = eval(input("What is the probability that player A wins a serve? "))
    b = eval(input("What is the probability that player B wins a serve? "))
    n = eval(input("How many games to simulate? "))
    return a, b, n

def main():
    print_intro()
    # Get user inputs
    probA, probB, n = get_inputs()
    # Play the games
    stats = SimStats()
    for _ in range(n):
        game = RBallGame(probA, probB) # create a new game
        game.play() # Play it
        stats.update(game) # Extract info
    # Print the results
    stats.print_report(n)

if __name__ == "__main__":
    main()
input("\nPress <Enter> to quit")