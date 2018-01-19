import pygame
from utils import Text


class HumanAvailableTimePerTurn():
    def __init__(self, maximumTime, fps):
        self.fps = fps
        self.maximumTime = maximumTime
        self.numbHelper = maximumTime * fps
        self.numbToDisplay = maximumTime

        self.black = (0, 0, 0)
        self.red = (255, 0, 0)

    def decreaseNumbHelper(self):
        self.numbHelper -= 1

    def resetTimer(self):
        self.numbHelper = self.maximumTime * self.fps
        self.numbToDisplay = self.maximumTime

    def isTimeZero(self, screen):
        if self.numbToDisplay == 0:
            text = Text(self.red, 40)
            text.display(screen, 100, 500, "Perdiste")
            self.numbToDisplay = 0

    def displayTime(self, screen, screenColor):
        pygame.draw.rect(screen, screenColor, (265, 15, 100, 50))
        text = Text(self.black, 30)
        text.display(screen, 315, 50, str(self.numbToDisplay))

        if self.numbToDisplay is not 0:
            if self.numbHelper == 0:
                self.numbHelper = self.fps * self.maximumTime
            elif self.numbHelper % self.fps == 0:
                self.numbToDisplay -= 1
