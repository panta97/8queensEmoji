import pygame
from utils import Text


class PaintBoardAndQueens():
    def __init__(self, screen, color1, color2, colorEdge, squares, size):
        self.screen = screen
        self.color1 = color1
        self.color2 = color2
        self.colorEdge = colorEdge
        self.squares = squares
        self.size = size

        # bad pratice
        self.boardPosX = 260
        self.boardPosY = 200

    def paintBoard(self, boardPosX, boardPosY):
        board = [[1, 0, 1, 0, 1, 0, 1, 0],
                 [0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 0, 1, 0, 1, 0, 1, 0],
                 [0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 0, 1, 0, 1, 0, 1, 0],
                 [0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 0, 1, 0, 1, 0, 1, 0],
                 [0, 1, 0, 1, 0, 1, 0, 1]]

        for j in range(self.squares):
            for i in range(self.squares):

                # draw the edges
                # 3 means the edge width
                pygame.draw.rect(self.screen, self.colorEdge, (self.size * i + boardPosX, self.size * j + boardPosY, self.size, self.size), 3)

                # draw the squares
                if board[i][j] == 1:
                    pygame.draw.rect(self.screen, self.color1, (self.size * i + boardPosX, self.size * j + boardPosY, self.size, self.size))
                else:
                    pygame.draw.rect(self.screen, self.color2, (self.size * i + boardPosX, self.size * j + boardPosY, self.size, self.size))

    def paintQueenAt(self, x, y):
        image = pygame.image.load("queen.png")
        image = pygame.transform.scale(image, (60, 56))
        self.screen.blit(image, (x * self.size + self.boardPosX, y * self.size + self.boardPosY))

    def repaintQueens(self, pieces):
        for piece in (pieces):
            self.paintQueenAt(piece[0], piece[1])


# it will help you for the game ending too
class BoardHint():

    def __init__(self, squares, boardPosX, boardPosY, size):
        self.squares = squares
        self.boardHint = []

        self.boardPosX = boardPosX
        self.boardPosY = boardPosY

        self.size = size

        for i in range(self.squares):
            self.boardHint.append([False] * self.squares)

    def getDiagonalPointsRight(self, boxx, boxy):
        listOfTuples = []
        # right diagonal
        x = boxx - self.squares
        y = boxy - self.squares

        while x < self.squares and y < self.squares:
            if x >= 0 and y >= 0:
                listOfTuples.append((x, y))
            x = x + 1
            y = y + 1

        # print(listOfTuples)
        return listOfTuples

    def getDiagonalPointsLeft(self, boxx, boxy):
        listOfTuples = []
        # right diagonal
        x = boxx - self.squares
        y = boxy + self.squares

        while x < self.squares and y >= 0:
            if x >= 0 and y < self.squares:
                listOfTuples.append((x, y))
            x = x + 1
            y = y - 1

        # print(listOfTuples)
        return listOfTuples[::-1]
        # return listOfTuples

    def changeBoardHintState(self, boxx, boxy):

        # print(boxx, boxy, squares)
        diagonalListRight = self.getDiagonalPointsRight(boxx, boxy)
        diagonalListLeft = self.getDiagonalPointsLeft(boxx, boxy)

        for j in range(self.squares):
            for i in range(self.squares):
                if diagonalListRight[0] == (i, j):
                    self.boardHint[i][j] = True
                    if len(diagonalListRight) != 1:
                        del diagonalListRight[0]
                    # else:
                    #     continue

                if diagonalListLeft[0] == (i, j):
                    self.boardHint[i][j] = True
                    if len(diagonalListLeft) != 1:
                        del diagonalListLeft[0]
                    # else:
                    #     continue

                elif boxx == i or boxy == j:
                    self.boardHint[i][j] = True

    def changeBoardHintStateInverse(self, pieces):
        self.restart()
        for piece in pieces:
            self.changeBoardHintState(piece[0], piece[1])

    def drawHints(self, screen, color):
        offset = 30
        for i in range(self.squares):
            for j in range(self.squares):
                if self.boardHint[i][j] == True:
                    pygame.draw.circle(screen, color, (self.boardPosX + offset + i * self.size, self.boardPosY + offset + j * self.size), 5)

    def getAvailableSpaces(self):
        counter = 0
        for i in range(self.squares):
            for j in range(self.squares):
                if self.boardHint[i][j] == False:
                    counter += 1
        return counter

    def restart(self):
        self.boardHint = []
        for i in range(self.squares):
            self.boardHint.append([False] * self.squares)
