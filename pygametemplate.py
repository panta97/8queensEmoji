import pygame
import sys
from pygame.locals import *  # like the std in c++

# initialize
pygame.init()

# set up the window
# constants
screen = pygame.display.set_mode((700, 700))
squares = 8
size = 60

color1 = (209, 139, 71)
color2 = (255, 206, 158)
colorEdge = (255, 255, 255)


# position of the board
boardPosX = 150
boardPosY = 150


# window title
pygame.display.set_caption('8 Queens')


# set up some colors
black = (0, 0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


# set screen background color
screen.fill(white)

# some basic figures
# pygame.draw.rect(screen, black, (200, 150, 100, 50))
# pygame.draw.line(screen, black, (60, 120), (120, 120), 4)
# pygame.draw.circle(screen, black, (300, 50), 20, 0)

# run the game loop


def main():

    helper = Helper()
    drawBoard = DrawBoard(screen, color1, color2, colorEdge)
    drawBoard.display()

    mousex = 0
    mousey = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos

        boxx, boxy = helper.getBoxAtPixel(mousex, mousey)

        if boxx != None and boxy != None:
            drawBoard.drawQueenAt(boxx, boxy, screen)

        pygame.display.update()


class DrawBoard():
    def __init__(self, screen, color1, color2, colorEdge):
        self.screen = screen
        self.color1 = color1
        self.color2 = color2
        self.colorEdge = colorEdge

    def display(self):
        board = [[1, 0, 1, 0, 1, 0, 1, 0],
                 [0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 0, 1, 0, 1, 0, 1, 0],
                 [0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 0, 1, 0, 1, 0, 1, 0],
                 [0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 0, 1, 0, 1, 0, 1, 0],
                 [0, 1, 0, 1, 0, 1, 0, 1]]

        for j in range(squares):
            for i in range(squares):

                # draw the edges
                # 3 means the edge width
                pygame.draw.rect(self.screen, self.colorEdge, (size * i + boardPosX, size * j + boardPosY, size, size), 3)

                # draw the squares
                if board[i][j] == 1:
                    pygame.draw.rect(self.screen, self.color1, (size * i + boardPosX, size * j + boardPosY, size, size))
                else:
                    pygame.draw.rect(self.screen, self.color2, (size * i + boardPosX, size * j + boardPosY, size, size))

    def drawQueenAt(self, x, y, screen):
        image = pygame.image.load("queen.png")
        image = pygame.transform.scale(image, (60, 56))
        screen.blit(image, (x * size + boardPosX, y * size + boardPosY))


class Helper():
    # def __init__(self):

    def leftTopCoordOfSquare(self, x, y):
        left = x * size + boardPosX
        top = y * size + boardPosY
        return (left, top)

    def getBoxAtPixel(self, x, y):
        for i in range(squares):
            for j in range(squares):
                left, top = self.leftTopCoordOfSquare(i, j)
                rect = pygame.Rect(left, top, size, size)
                if rect.collidepoint(x, y):
                    return(i, j)
        return(None, None)


if __name__ == '__main__':
    main()
