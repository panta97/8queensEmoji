import pygame
from utils import Text


class PlayersDetails():
    def __init__(self):
        self.humanScore = 0
        self.computerScore = 0
        self.humanConsecutiveMistakes = 0
        self.numberOfQueens = 0

        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)

    def addPointsToHuman(self):
        self.humanScore += 10

    def addPointsToComputer(self):
        self.computerScore += 10

    def substractPointsToHuman(self):
        self.humanScore -= 5
        self.humanConsecutiveMistakes += 1

    def resetHumanConsecutiveMistakes(self):
        self.humanConsecutiveMistakes = 0

    def resetScores(self):
        self.humanScore = 0
        self.computerScore = 0

    def refreshHumanScore(self, screen, screenColor):
        positionX = 440
        positionY = 100

        text = Text(self.black, 60)
        pygame.draw.rect(screen, screenColor, (positionX - 40, positionY - 40, 80, 80))
        text.display(screen, positionX, positionY, str(self.humanScore))
        pygame.display.update()

    def refreshComputerScore(self, screen, screenColor):
        positionX = 540
        positionY = 100

        text = Text(self.black, 60)
        pygame.draw.rect(screen, screenColor, (positionX - 40, positionY - 40, 80, 80))
        text.display(screen, positionX, positionY, str(self.computerScore))
        pygame.display.update()

    def displayGameOverIfIsThreeConsecutiveMistakes(self, screen):
        if self.humanConsecutiveMistakes == 3:
            text = Text(self.red, 40)
            text.display(screen, 100, 500, "Perdiste")

    def displayGameEnding(self, screen):
        if self.humanScore < self.computerScore:
            text = Text(self.red, 40)
            text.display(screen, 100, 500, "Perdiste")
        elif self.humanScore > self.computerScore:
            text = Text(self.blue, 40)
            text.display(screen, 100, 500, "Ganaste")
        elif self.humanScore == self.computerScore:
            text = Text(self.green, 40)
            text.display(screen, 100, 500, "Empate")
