"""GOOD CODE INIMGEN"""
from random import randint


class Dice:
    # Class representing a dice
    def __init__(self):
        self.roll()

    # Rolls the dice and stores the values.
    def roll(self):
        self.dice = [randint(1, 6) for _ in range(2)]

    def returnValues(self):
        return self.dice[:]


class SkunkApp:
    # Main application class
    def __init__(self, interface):
        self.dice = Dice()
        self.interface = interface
        self.players = []
        self.createPlayer()

    # Runs the game until the end condition is met
    def run(self):
        while not self.interface.round >= 4:
            self.interface.newRound()
            self.refreshPlayers()
            print("Round: {}".format(self.interface.round + 1))
            print("\n")
            self.playRound()
        gameSummary(self.players)

    # Simulates a round of the game to get scores
    def playRound(self):
        books = self.interface.round
        while not self.roundOver():
            for player in self.players:
                if player.play:
                    values = self.rollDice(player)
                    if values != [0, 0]:
                        x, y = values[0], values[1]
                        if x == 1 or y == 1:
                            if x == 1 and y == 1:
                                player.resetRoundScores(books)
                            else:
                                player.resetRoundScore()
                        else:
                            player.increaseScore(x + y, books)
                        currentScoresCount(values, self.players)
        for player in self.players:
            player.tallyRound(books)

    def rollDice(self, player):
        if rollAgain(player.name):
            self.dice.roll()
            return self.dice.returnValues()
        else:
            player.deactivate()
            return [0, 0]

    def refreshPlayers(self):
        for player in self.players:
            player.deactivate()
            player.roundScore = 0

    def roundOver(self):
        return all(not player.play for player in self.players)

    def createPlayer(self):
        self.players = [Player(name) for name in getPlayerNames()]


class Player:
    # Class representing a player
    def __init__(self, name):
        self.name = name
        self.roundScore = 0
        self.totalScore = 0
        self.roundScores = [0] * 5
        self.play = True

    def reactivate(self):
        self.play = True

    def deactivate(self):
        self.play = False

    def active(self):
        return self.play

    def resetRoundScores(self, books):
        previousRoundScores = sum(self.roundScores)
        self.totalScore -= previousRoundScores
        self.roundScores[:books] = [0] * books
        self.play = False

    def resetRoundScore(self):
        self.totalScore -= self.roundScore
        self.roundScore = 0
        self.play = False

    def increaseScore(self, score, books):
        self.totalScore += score
        previousRoundScores = sum(self.roundScores[:books])
        self.roundScore = self.totalScore - previousRoundScores

    def tallyRound(self, book):
        self.roundScores[book] = self.roundScore


def setDice(values):
    print(f"You rolled {values}.")
    print("\n")


def getPlayerNames():
    totalPlayers = []
    player_name = input("Enter a players name (<Enter> to Continue) >> ")
    while player_name != '':
        totalPlayers.append(player_name)
        player_name = input("Enter another player's name (Press <Enter> to continue) >> ")
    return [name for name in totalPlayers if name.strip()]


def finalScores(players):
    # Prints final scores of the players
    print(f"Name: {'S':>10}{'K':>10}{'U':>10}{'N':>10}{'K':>10}{'Total':>10}")
    print("-------------------------------------------------------------------")
    for player in players:
        name = player.name
        scores = " ".join([f"{score:>10}" for score in player.roundScores])
        totalScore = player.totalScore
        print(f"{name:5}:{scores}{totalScore:>10}")


def gameSummary(players):
    print("The game is over.")
    finalScores(players)


def currentScoresCount(values, players):
    # Prints current scores of the players to console
    for player in players:
        name, roundScore, totalScore = player.name, player.roundScore, player.totalScore
        print("Player: {0}    Score: {1}     Total: {2}".format(name, roundScore, totalScore))
    setDice(values)


def rollAgain(name):
    # Asks if the player wants to roll again
    while True:
        ans = input("Do you wish to roll again {}? >> ".format(name)).strip().lower()
        if ans.startswith('y'):
            return True
        elif ans.startswith('n'):
            return False
        else:
            print("Sorry, I don't understand.")


class TextInterface:
    # Console user interface.
    def __init__(self):
        self.round = -1

    def newRound(self):
        self.round += 1
        print(f"Entering Round {self.__whichRound()}")
        return self.round

    # Defines which round is it based on the SKUNK game name
    def __whichRound(self):
        letter = ["S", "K", "U", "N", "K"]
        return letter[self.round]


def main():
    interface = TextInterface()
    dice_game = SkunkApp(interface)
    dice_game.run()


main()
