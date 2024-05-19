from random import randint


class Dice:
    def __init__(self):
        self.die1 = 0
        self.die2 = 0

    def roll_dice(self):
        self.die1 = randint(1, 6)
        self.die2 = randint(1, 6)

    def values(self):
        return [self.die1, self.die2]


class SkunkApp:
    def __init__(self):
        self.dice = Dice()
        self.players = []

    def play(self):
        print("Welcome to Skunk Game!")
        self.make_players()
        round_num = 0
        while round_num < 5:
            print("\nRound: " + str(round_num + 1))
            self.play_round(round_num)
            round_num += 1
        print("\nGame over!")
        self.game_summary()

    def play_round(self, round_num):
        for player in self.players:
            print("\nPlayer: " + player.get_name())
            round_score = 0
            while True:
                choice = input("Do you want to roll the dice? (yes/no): ").lower()
                if choice == "yes":
                    self.dice.roll_dice()
                    roll = self.dice.values()
                    print("Dice rolled: " + str(roll[0]) + ", " + str(roll[1]))
                    if roll == [1, 1]:
                        print("You rolled double ones! Round score reset.")
                        player.reset_round_scores(round_num)
                        round_score = 0
                        break
                    elif 1 in roll:
                        print("You rolled a one! Round over.")
                        round_score = 0
                        break
                    else:
                        round_score += sum(roll)
                        print("Round score: " + str(round_score))
                else:
                    print("Starting a new round.")
                    break
            player.increment_score(round_score, round_num)

    def make_players(self):
        num_players = int(input("Enter the number of players: "))
        for i in range(num_players):
            player_name = input("Enter player " + str(i + 1) + " name: ")
            self.players.append(Player(player_name))

    def game_summary(self):
        for player in self.players:
            print("Player: " + player.get_name() + ", Total Score: " + str(player.get_total_score()))


class Player:
    def __init__(self, name):
        self.name = name
        self.total_score = 0
        self.round_scores = [0] * 5

    def get_name(self):
        return self.name

    def increment_score(self, score, round_num):
        self.total_score += score
        self.round_scores[round_num] = score

    def reset_round_scores(self, round_num):
        prev_round_scores = sum(self.round_scores)
        self.total_score -= prev_round_scores
        for i in range(round_num + 1):
            self.round_scores[i] = 0

    def get_total_score(self):
        return self.total_score


def main():
    game = SkunkApp()
    game.play()


if __name__ == "__main__":
    main()
