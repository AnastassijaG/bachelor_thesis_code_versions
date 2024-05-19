from random import random
# BAD #
class Player:
    def __init__(self, prob):
        self.prob = prob
        self.score = 0

    def winsServe(self):
        if random() < self.getProb():
            wins = True
        else:
            wins = False
        return wins

    def getProb(self):
        return self.prob

    def getScore(self):
        return self.score

    def setScore(self, score):
        self.score = score


class RBallGame:
    def __init__(self, probA, probB):
        self.playerA = Player(probA)
        self.playerB = Player(probB)
        self.server = self.playerA

    def play(self):
        while not self.isOver():
            if random() < self.server.getProb():
                serverWinsServe = True
            else:
                serverWinsServe = False
            if serverWinsServe:
                currentScore = self.server.getScore()
                incrementScore = currentScore + 1
                self.server.setScore(incrementScore)
            else:
                serverA = self.server == self.playerA
                if serverA:
                    self.server = self.playerB
                else:
                    self.server = self.playerA

    def isOver(self):
        a, b = self.getScores()
        if a == 15 or b == 15:
            return True
        if a == 7 and b == 0:
            return True
        if b == 7 and a == 0:
            return True
        return False

    def getScores(self):
        scoreA = self.playerA.getScore()
        scoreB = self.playerB.getScore()
        return scoreA, scoreB


class SimStats:
    def __init__(self):
        self.winsA = 0
        self.winsB = 0
        self.shutsA = 0
        self.shutsB = 0

    def update(self, aGame):
        a, b = aGame.getScores()
        if a > b:
            self.winsA = self.winsA + 1
            if b == 0:
                self.shutsA = self.shutsA + 1
        else:
            self.winsB = self.winsB + 1
            if a == 0:
                self.shutsB = self.shutsB + 1

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
            averageWins = float(wins) / n
            print(template.format(label, wins, averageWins, shuts, shutStr))
        else:
            shutStr = "{0:4.1%}".format(float(shuts) / wins)
            averageWins = float(wins) / n
            print(template.format(label, wins, averageWins, shuts, shutStr))



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
input("\nPress <Enter> to quit")