from random import random

#BAD CODE#
class Game:
    def __init__(self, probA, probB):
        self.playerA = Player(probA)
        self.playerB = Player(probB)
        self.server = self.playerA

    def playGame(self):
        while not self.isOver():
            if random() < self.server.prob:
                self.playerA.incScore()
            else:
                self.playerB.incScore()
        if self.playerA.score > self.playerB.score:
            self.playerA.incGames()
        else:
            self.playerB.incGames()

    def isOver(self):
        scoreDiff = abs(self.playerA.score - self.playerB.score)
        return (self.playerA.score >= 4 or self.playerB.score >= 4) and scoreDiff >= 2

class Player:
    def __init__(self, prob):
        self.prob = prob
        self.score = 0
        self.games = 0

    def incScore(self):
        self.score += 1

    def incGames(self):
        self.games += 1

class Tournament:
    def __init__(self, probA, probB, num_matches):
        self.probA = probA
        self.probB = probB
        self.num_matches = num_matches
        self.stats = Stats()

    def simulate(self):
        for _ in range(self.num_matches):
            match = Game(self.probA, self.probB)
            match.playGame()
            self.stats.update(match)

class Stats:
    def __init__(self):
        self.winsA = 0
        self.winsB = 0

    def update(self, match):
        if match.playerA.games > match.playerB.games:
            self.winsA += 1
        else:
            self.winsB += 1

    def printReport(self):
        total = self.winsA + self.winsB
        print("Summary of", total, "matches:\n")
        print("         Wins (% total)")
        print("---------------------------")
        print("Player A: ", self.winsA, "(", (self.winsA / total) * 100, "%)")
        print("Player B: ", self.winsB, "(", (self.winsB / total) * 100, "%)")

def main():
    probA = float(input("Enter the probability of player A winning a serve: "))
    probB = float(input("Enter the probability of player B winning a serve: "))
    num_matches = int(input("Enter the number of matches to simulate: "))
    tourney = Tournament(probA, probB, num_matches)
    tourney.simulate()
    tourney.stats.printReport()

if __name__ == "__main__":
    main()