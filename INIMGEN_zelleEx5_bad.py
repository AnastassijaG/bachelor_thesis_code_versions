import copy
from random import randrange


class Dice:
    def __init__(self):
        self.dice = [0, 0]
        self.roll_dice()

    def roll_dice(self):
        dice_count = len(self.dice)
        for i in range(dice_count):
            dice_value = randrange(1, 7)
            self.dice[i] = dice_value
        return copy.deepcopy(self.dice)

class SkunkApp:
    def __init__(self, interface):
        self.dice = Dice()
        self.interface = interface
        self.players = []
        self.make_players()

    def runGame(self):
        while not self.GameOver():
            self.interface.newRound()
            for player in self.players:
                player.deactivate()
                player.roundScoreOnly()
            print(f"Round: {self.interface.getRound() + 1}")
            print("\n")

            books = self.interface.getRound()
            while not self.Round_Over():
                for player in self.players:
                    if not player.isActive() == False:
                        values = self.DoRoll(player)
                        if values != [0, 0]:
                            x = values[0]
                            y = values[1]
                            player.countScoreOrReset(x, y, books)
                            for player in self.players:
                                 name = player.getName()
                                 roundScore = player.get_rScore()
                                 total_score = player.getTotalScore()
                                 print(f"Player: {name}  Score: {roundScore}    Total: {total_score}")
                            print(f"You rolled {values}")
                            print("\n")

            for player in self.players:
                player.tallyRound(books)

        print("The game is over")
        self.interface.finalScores(self.players)

    def make_players(self):
        players = self.interface.getPlayerNames()
        for player_name in players:
            this_player = Player(player_name)
            self.players.append(this_player)

    def Round_Over(self):
        over = True
        for player in self.players:
            if player.isActive():
                over = False
        return over

    def DoRoll(self, player):
        if self.interface.rollDiceAgain(player.getName()):
            values = self.dice.roll_dice()
            return values
        else:
            player.deactivate()
            return [0, 0]

    def GameOver(self):
        if self.interface.getRound() >= 4:
            return True


class Player:
    def __init__(self, name):
        self.name = name
        self.round_score = 0
        self.total_score = 0
        self.round_scores = [0] * 5
        self.play = True

    def getName(self):
        name = self.name
        return name

    def deactivate(self):
        self.play = False

    def isActive(self):
        is_player_active = self.play
        return is_player_active

    def tallyRound(self, book):
        current_score = self.get_rScore()
        self.round_scores[book] = current_score

    def get_rScore(self):
        self_round_score = self.round_score
        return self_round_score

    def getRoundScores(self):
        this_round_scores = self.round_scores
        return this_round_scores

    def getTotalScore(self):
        total_score = self.total_score
        return total_score

    def reactivate(self):
        self.play = True

    def roundScoreOnly(self):
        self.round_score = 0

    def rScoreOnly(self):
        self.rScore = 0


    def countScoreOrReset(self, x, y, books):
        if x == 1 and y == 1:
            previousRoundScores = 0
            for number in self.round_scores:
                previousRoundScores = previousRoundScores + number
            self.total_score = self.total_score - previousRoundScores
            for i in range(books):
                self.round_scores[i] = 0
            self.play = False
        elif x == 1 or y == 1:
            self.total_score = self.total_score - self.round_score
            self.round_score = 0
            self.play = False
        elif not (x == 1 and y == 1) and not (x == 1 or y == 1):
            score = x + y
            self.total_score = self.total_score + score
            previousRoundScores = 0
            for number in self.round_scores[0:books]:
                previousRoundScores = previousRoundScores + number
            self.round_score = self.total_score - previousRoundScores


class TextInterface:
    def __init__(self):
        self.round = -1

    def getRound(self):
        round_nr = self.round
        return round_nr

    def gameSummary(self, players):
        print("The game is over.")
        self.finalScores(players)

    def setDice(self, values):
        print("You rolled {}.".format(values))
        print("\n")

    def rollDiceAgain(self, name):
        ans = None
        while not ans:
            ans = input(f"Do you wish to roll again {name}: ")
            if ans[0] == 'y' or ans[0] == 'Y':
                return True
            elif ans[0] == 'n' or ans[0] == 'N':
                return False
            elif ans[0] != 'y' and ans[0] != 'Y' and ans[0] != 'n' and ans[0] != 'N':
                print("Sorry, i do not understand you.")
                continue

    def getPlayerNames(self):
        total_players = []
        current_input = "Placeholder"
        while current_input != '':
            current_input = input("Please enter a player's name (Press <Enter> to continue) >> ")
            if current_input:
                total_players.append(current_input)
                if len(current_input) > 10:
                    print("Next time choose a shorter name please")
                elif len(current_input) < 3:
                    print("Next time choose a longer name please")

        return total_players

    def newRound(self):
        self.round = self.round + 1
        print()
        print(f"Entering Round {self.round_nr()}")

    def round_nr(self):
        letters = ["S", "K", "U", "N", "K"]
        current_round = self.round
        current_letter = letters[current_round]
        return current_letter

    def finalScores(self, players):
        print("Name: {0:>10}{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}".format("S", "K" , "U", "N", "K",
                                                                        "Total"))
        print("-------------------------------------------------------------------")
        for player in players:
            scores = player.getRoundScores()
            name = player.getName()
            totscore = player.getTotalScore()
            print("{0:5}:{1:>10}{2:>10}{3:>10}{4:>10}{5:>10}{6:>10}".format(name, scores[0], scores[1],scores[2],
                                                                            scores[3], scores[4], totscore))

def main():
    inter = TextInterface()
    app = SkunkApp(inter)
    app.runGame()


main()


