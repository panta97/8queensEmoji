import pygame
import sys
import random
import copy
from itertools import *
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

    board = Board(1)

    boardHint = BoardHint(squares)

    mousex = 0
    mousey = 0
    hintEnable = True

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos

                boxx, boxy = helper.getBoxAtPixel(mousex, mousey)

                if boxx != None and boxy != None:
                    # if new placed piece is attacking any other queen
                    if board.isAttackingAny((boxx, boxy)):
                        print("game over")
                    else:
                        drawBoard.drawQueenAt(boxx, boxy, screen)
                        board.PlaceQueen(boxx, boxy)
                        boardHint.changeBoardHintState(boxx, boxy)

                        # gets you the new board
                        newboard = computerTurn(board)

                        if newboard is None:
                            print("You Win")

                        else:

                            newQueenPosition = boardDistinc(board.getBoard(), newboard)
                            boxx, boxy = newQueenPosition

                            drawBoard.drawQueenAt(boxx, boxy, screen)
                            board.PlaceQueen(boxx, boxy)
                            boardHint.changeBoardHintState(boxx, boxy)

                            print(newQueenPosition)

                if hintEnable == True:
                    boardHint.drawHints(screen)

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


class Board:
    ''' A class to represent the checker board'''

    def __init__(self, n):  # Initializes the class
        self.board = [[None for i in range(8)] for i in range(8)]
        self.pieces = set()

    def __str__(self):
        '''Allows us to print the board'''
        S = ''
        for i in self.board:
            S += str(i) + '\n'
        return S

    def PlaceQueen(self, row, column):
        '''Places a queen at row,column'''
        self.pieces.add((row, column))
        self.board[row][column] = 'Q'

    def RemoveQueen(self, row, column):
        '''Removes a queen from a given 'row' and 'column' '''
        self.board[row][column] = None
        self.pieces.remove((row, column))

    def isAttacking(self, piece1, piece2):
        '''Checks if piece1 attacks piece2'''
        if piece1[0] == piece2[0] or piece1[1] == piece2[1]:  # Check if they are in same row or col
            return True
        '''Time to check if they are attacking diagonally
         This can be done efficiently via simple algebra
         The two pices are on the same diagonal if they
         satisfy an equation of a line containing the two points'''
        x1, y1, x2, y2 = piece1[1], piece1[0], piece2[1], piece2[0]
        m = float(y2 - y1) / (x2 - x1)
        if abs(m) != 1.0:
            return False
        else:
            b = y2 - m * x2
            return y1 == m * x1 + b

    def isAttackingAny(self, piece):
        '''Checks if piece is being atacked by
           any other piece in the board'''
        for piece1 in self.pieces:
            if self.isAttacking(piece, piece1):
                return True
        return False

    def getBoard(self):
        return self.board


def NQueens(board, n):
    if n == 0:
        return [board]
    solutions = []
    i = 0
    for piece1 in product(range(8), repeat=2):
        if piece1 in board.pieces:
            continue
        if not board.isAttackingAny(piece1):
            i += 1
            fresh = copy.deepcopy(board)
            fresh.PlaceQueen(piece1[0], piece1[1])
            solutions += NQueens(fresh, n - 1)
    return solutions


def boardDistinc(currentBoard, newBoard):

    for j in range(squares):
        for i in range(squares):
            if currentBoard[j][i] != newBoard[j][i]:
                return (j, i)


def computerTurn(board):
    solutions = NQueens(board, 1)
    numberOfSolutions = len(solutions) - 1

    # in case there are no longer solutions
    if numberOfSolutions <= 0:
        return None

    randomSolutionIndex = random.randint(0, numberOfSolutions)
    chosenSolution = solutions[randomSolutionIndex]
    return chosenSolution.getBoard()


class BoardHint():

    def __init__(self, squares):
        self.squares = squares
        self.boardHint = []
        for i in range(squares):
            self.boardHint.append([False] * squares)

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

        while x < squares and y >= 0:
            if x >= 0 and y < self.squares:
                listOfTuples.append((x, y))
            x = x + 1
            y = y - 1

        print(listOfTuples)
        return listOfTuples[::-1]
        # return listOfTuples

    def changeBoardHintState(self, boxx, boxy):

        print(boxx, boxy, squares)
        diagonalListRight = self.getDiagonalPointsRight(boxx, boxy)
        diagonalListLeft = self.getDiagonalPointsLeft(boxx, boxy)

        for j in range(squares):
            for i in range(squares):
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

    def drawHints(self, screen):

        offset = 30

        for i in range(squares):
            for j in range(squares):
                if self.boardHint[i][j] == True:
                    pygame.draw.circle(screen, (0, 0, 0), (boardPosX + offset + i * size, boardPosY + offset + j * size), 5)


if __name__ == '__main__':
    main()
