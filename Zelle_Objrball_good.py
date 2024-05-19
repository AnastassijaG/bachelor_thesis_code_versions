from random import random

# GOOD CODE #
class Player:
    def __init__(self, probability):
        self.probability = probability
        self.score = 0

    def wins_serve(self):
        return random() <= self.probability

    def increment_score(self):
        self.score += 1

    def get_score(self):
        return self.score

class RacquetballGame:
    def __init__(self, probability_a, probability_b):
        self.player_a = Player(probability_a)
        self.player_b = Player(probability_b)
        self.server = self.player_a

    def play(self):
        while not self.is_over():
            self.play_point()

    def play_point(self):
        if self.server.wins_serve():
            self.server.increment_score()
        else:
            self.change_server()

    def is_over(self):
        return max(self.player_a.get_score(), self.player_b.get_score()) >= 15

    def change_server(self):
        self.server = self.player_b if self.server == self.player_a else self.player_a

class GameStats:
    def __init__(self):
        self.wins = {'A': 0, 'B': 0}
        self.shutouts = {'A': 0, 'B': 0}

    def update(self, game):
        winner = 'A' if game.player_a.get_score() > game.player_b.get_score() else 'B'
        loser = 'B' if winner == 'A' else 'A'

        self.wins[winner] += 1
        if game.player_b.get_score() == 0:
            self.shutouts[winner] += 1

    def print_report(self, total_games):
        print(f"Summary of {total_games} games:\n")
        print("         wins (% total)  shutouts (% wins)   ")
        print("----------------------------------------")
        for player in ['A', 'B']:
            wins = self.wins[player]
            shutouts = self.shutouts[player]
            win_percentage = (wins / total_games) * 100 if total_games != 0 else 0
            shutout_percentage = (shutouts / wins) * 100 if wins != 0 else 0
            print(f"Player {player}: {wins:5}    ({win_percentage:.1f}%)  {shutouts:11}  ({shutout_percentage:.1f}%)")

def print_intro():
    print("This program simulates games of racquetball between two")
    print('players called "A" and "B". The ability of each player is')
    print("indicated by a probability (a number between 0 and 1) that")
    print("the player wins the point when serving. Player A always")
    print("has the first serve. \n")

def get_inputs():
    probability_a = float(input("What is the probability that player A wins a serve? "))
    probability_b = float(input("What is the probability that player B wins a serve? "))
    num_games = int(input("How many games to simulate? "))
    return probability_a, probability_b, num_games

def main():
    print_intro()
    probability_a, probability_b, num_games = get_inputs()

    stats = GameStats()
    for _ in range(num_games):
        game = RacquetballGame(probability_a, probability_b)
        game.play()
        stats.update(game)

    total_games = num_games
    stats.print_report(total_games)

if __name__ == "__main__":
    main()
