from random import random

# BAD CODE #
# Poorly structured Player class
class Player:
    def __init__(self, prob):
        self.prob = prob
        self.score = 0

    def winsServe(self):
        if random() <= self.prob:
            return True
        else:
            return False

    def incScore(self):
        self.score += 1

    def getScore(self):
        return self.score


class RBallGame:
    def __init__(self, probA, probB):
        self.playerA = Player(probA)
        self.playerB = Player(probB)
        self.server = self.playerA

    def play(self):
        while not self.isOver():
            if self.server.winsServe():
                self.server.incScore()
            else:
                self.changeServer()

    def isOver(self):
        a, b = self.getScores()
        if a == 15 or b == 15:
            return True
        elif (a == 7 and b == 0) or (b == 7 and a == 0):
            return True
        else:
            return False

    def changeServer(self):
        if self.server == self.playerA:
            self.server = self.playerB
        else:
            self.server = self.playerA

    def getScores(self):
        return self.playerA.getScore(), self.playerB.getScore()


class SimStats:
    def __init__(self):
        self.winsA = 0
        self.winsB = 0
        self.shutsA = 0
        self.shutsB = 0

    def update(self, aGame):
        a, b = aGame.getScores()
        if a > b:
            self.winsA += 1
            if b == 0:
                self.shutsA += 1
        else:
            self.winsB += 1
            if a == 0:
                self.shutsB += 1

    def printReport(self):
        n = self.winsA + self.winsB
        print("Summary of", n, "games:\n")
        print("         wins (% total)  shutouts (% wins)   ")
        print("----------------------------------------")
        self.printLine("A", self.winsA, self.shutsA, n)
        self.printLine("B", self.winsB, self.shutsB, n)

    def printLine(self, label, wins, shuts, n):
        template = "Player {0}:{1:5}    ({2:5.1%})  {3:11}  ({4})"
        if wins == 0:
            shutStr = "-----"
        else:
            shutStr = "{0:4.1%}".format(float(shuts) / wins)
        print(template.format(label, wins, float(wins) / n, shuts, shutStr))


def printIntro():
    print("This program simulates games of racquetball between two")
    print('players called "A" and "B". The ability of each player is')
    print("indicated by a probability (a number between 0 and 1) that")
    print("the player wins the point when serving. Player A always")
    print("has the first serve. \n")


def getInputs():
    a = eval(input("What is the prob. player A wins a serve? "))
    b = eval(input("What is the prob. player B wins a serve? "))
    n = eval(input("How many games to simulate? "))
    return a, b, n


def main():
    printIntro()

    probA, probB, n = getInputs()
    stats = SimStats()
    for i in range(n):
        theGame = RBallGame(probA, probB)
        theGame.play()
        stats.update(theGame)

    stats.printReport()

if __name__ == "__main__":
    main()