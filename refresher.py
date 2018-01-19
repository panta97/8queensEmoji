import pygame
from utils import Text


class GameStateRefresher():
    def displayTextOptions(self, screen, textColor):
        text = Text(textColor, 30)
        text.display(screen, 100, 300, "hint - H")
        text.display(screen, 100, 350, "restart - R")
        text.display(screen, 100, 400, "undo - U")

        # YOU
        black = (0, 0, 0)
        textHuman = Text(black, 70)
        textHuman.display(screen, 315, 100, "YOU")

    def displayEmoji(self, screen, state, screenColor):
        thinkingEmoji = pygame.image.load("thinking.png")
        happyEmoji = pygame.image.load("happy.png")

        if state is "thinking":
            screen.blit(thinkingEmoji, (600, 30))
            pygame.display.update()
            pygame.time.wait(1000)
        elif state is "smiling":
            pygame.draw.rect(screen, screenColor, (600, 30, 200, 150))
            screen.blit(happyEmoji, (600, 30))

    def disableUndoText(self, screen, color, screenColor):
        pygame.draw.rect(screen, screenColor, (30, 380, 140, 50))
        text = Text(color, 30)
        text.display(screen, 100, 400, "undo - U")
