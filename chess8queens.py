import pygame
import sys
import random
import copy
import time
from itertools import *
from pygame.locals import *  # like the std in c++

# initialize
pygame.init()

# set up the window
# constants
screen = pygame.display.set_mode((800, 800))
squares = 8
size = 60

color2 = (209, 139, 71)
color1 = (255, 206, 158)
colorEdge = (255, 255, 255)


# position of the board
boardPosX = 260
boardPosY = 200

# window title
pygame.display.set_caption('8 Queens')


# set up some colors
black = (0, 0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (180, 180, 180)
screenColor = (178, 203, 216)

FPS = 10
fpsClock = pygame.time.Clock()

# set screen background color
screen.fill(screenColor)

# some basic figures
# pygame.draw.rect(screen, black, (200, 150, 100, 50))
# pygame.draw.line(screen, black, (60, 120), (120, 120), 4)
# pygame.draw.circle(screen, black, (300, 50), 20, 0)

# run the game loop


def main():

    helper = Helper()
    drawBoard = DrawBoard(screen, color1, color2, colorEdge)
    drawBoard.display()
    displayText(screen)
    board = Board(1)

    boardHint = BoardHint(squares)

    # mousex = 0
    # mousey = 0
    hintEnable = False
    undoMoveEnable = False
    lastPiecePlaced = None

    # in order to enable the toggle hit feature i'll create the pieces variable
    pieces = None

    # this class takes care of the computer and humann scores
    playersdetails = playersDetails()
    humanAvailableTimePerTurn = HumanAvailableTimePerTurn(30, FPS)

    while True:
        # para las teclas que seran presionadas
        pressed = pygame.key.get_pressed()
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

                        playersdetails.substractPointsToHuman()
                        playersdetails.displayGameOverIfIsThreeConsecutiveMistakes(screen)
                        playersdetails.refreshHumanScore(screen)

                    else:
                        drawBoard.drawQueenAt(boxx, boxy, screen)
                        board.PlaceQueen(boxx, boxy)
                        boardHint.changeBoardHintState(boxx, boxy)

                        # gets you the new board

                        newboard = computerTurn(board)
                        pieces = board.getPieces()

                        # print(newboard)

                        playersdetails.addPointsToHuman()
                        playersdetails.resetHumanConsecutiveMistakes()
                        playersdetails.refreshHumanScore(screen)

                        # undoTextRefreshColor(screen)
                        # pygame.draw.rect(screen, screenColor, (30, 380, 140, 50))
                        # text = Text(black, 30)
                        # text.display(screen, 100, 400, "undo - U")

                        if newboard is None:
                            print("You Win")

                            playersdetails.displayGameEnding(screen)

                        else:

                            newQueenPosition = boardDistinc(board.getBoard(), newboard)
                            # el boardDistinc te devuelve la posicion donde se pueso la nueva pieza
                            boxx, boxy = newQueenPosition

                            displayEmoji(screen, "thinking")
                            drawBoard.drawQueenAt(boxx, boxy, screen)
                            displayEmoji(screen, "smiling")

                            board.PlaceQueen(boxx, boxy)
                            boardHint.changeBoardHintState(boxx, boxy)

                            pieces = board.getPieces()
                            print(pieces)
                            # print(newQueenPosition)

                            lastPiecePlaced = (boxx, boxy)

                            # para deshacer la jugada una vez por turno
                            if undoMoveEnable is False:
                                undoMoveEnable = True

                            playersdetails.addPointsToComputer()
                            playersdetails.refreshComputerScore(screen)

                # necesitas este hint tambien para mostraar las pistas despues de volverlas a activarlas
                if hintEnable == True:
                    boardHint.drawHints(screen)

            # TOGGLE HINT
            if pressed[pygame.K_h]:
                hintEnable = toggleVal(hintEnable)
                if hintEnable == True:
                    boardHint.drawHints(screen)
                else:

                    if pieces is None:
                        continue
                    drawBoard.display()
                    # pieces significa la posiciones donde estan las reynas
                    for piece in (pieces):
                        drawBoard.drawQueenAt(piece[0], piece[1], screen)
                        # print(piece[0])

            # RESTART GAME
            if pressed[pygame.K_r]:
                # print("you have to restart the game")
                # print(board)
                board.restarBoard()
                boardHint.restart()
                pieces = None

                # print(board)
                playersdetails.resetScores()
                playersdetails.refreshHumanScore(screen)
                playersdetails.refreshComputerScore(screen)
                drawBoard.display()

            # UNDO MOVE'S OPPONENT
            if pressed[pygame.K_u]:

                if undoMoveEnable:
                    board.RemoveQueen(lastPiecePlaced[0], lastPiecePlaced[1])

                    print(board.pieces)
                    print(lastPiecePlaced[0], lastPiecePlaced[1])

                    drawBoard.display()
                    for piece in (board.pieces):
                        drawBoard.drawQueenAt(piece[0], piece[1], screen)

                    pygame.draw.rect(screen, screenColor, (30, 380, 140, 50))
                    text = Text(gray, 30)
                    text.display(screen, 100, 400, "undo - U")

                    undoMoveEnable = toggleVal(undoMoveEnable)

                # print(pieces)
                # print(board.pieces)

        humanAvailableTimePerTurn.decreaseNumbHelper()
        humanAvailableTimePerTurn.displayTime(screen, screenColor)
        fpsClock.tick(FPS)
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

    def getPieces(self):
        return self.pieces

    def restarBoard(self):

        self.board = [[None for i in range(8)] for i in range(8)]
        self.pieces = set()


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
    # print(len(solutions))
    numberOfSolutions = len(solutions) - 1

    # in case there are no longer solutions
    if numberOfSolutions < 0:
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

        # print(listOfTuples)
        return listOfTuples[::-1]
        # return listOfTuples

    def changeBoardHintState(self, boxx, boxy):

        # print(boxx, boxy, squares)
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

    def restart(self):
        self.boardHint = []
        for i in range(squares):
            self.boardHint.append([False] * squares)


class Text(object):
    def __init__(self, color, fontSize):
        self.color = color
        self.fontSize = fontSize

    def display(self, screen, x, y, text):
        fontObj = pygame.font.Font('freesansbold.ttf', self.fontSize)
        textSurfaceObj = fontObj.render(text, True, self.color)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (x, y)
        screen.blit(textSurfaceObj, textRectObj)  # this part is important


def displayText(screen):
    text = Text(black, 30)
    text.display(screen, 100, 300, "hint - H")
    text.display(screen, 100, 350, "restart - R")
    text.display(screen, 100, 400, "undo - U")

    # YOU
    textHuman = Text(black, 70)
    textHuman.display(screen, 315, 100, "YOU")


def displayEmoji(screen, state):
    thinkingEmoji = pygame.image.load("thinking.png")
    happyEmoji = pygame.image.load("happy.png")

    if state is "thinking":
        screen.blit(thinkingEmoji, (600, 30))
        pygame.display.update()
        pygame.time.wait(1000)
    elif state is "smiling":
        pygame.draw.rect(screen, screenColor, (600, 30, 200, 150))
        screen.blit(happyEmoji, (600, 30))


# def gameStates(board):

def toggleVal(value):
    if value is True:
        return False
    else:
        return True

# last implementations


class playersDetails():
    def __init__(self):
        self.humanScore = 0
        self.computerScore = 0
        self.humanConsecutiveMistakes = 0
        self.numberOfQueens = 0

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

    def refreshHumanScore(self, screen):
        positionX = 440
        positionY = 100

        text = Text(black, 60)
        pygame.draw.rect(screen, screenColor, (positionX - 40, positionY - 40, 80, 80))
        text.display(screen, positionX, positionY, str(self.humanScore))
        pygame.display.update()

    def refreshComputerScore(self, screen):
        positionX = 540
        positionY = 100

        text = Text(black, 60)
        pygame.draw.rect(screen, screenColor, (positionX - 40, positionY - 40, 80, 80))
        text.display(screen, positionX, positionY, str(self.computerScore))
        pygame.display.update()

    def displayGameOverIfIsThreeConsecutiveMistakes(self, screen):
        if self.humanConsecutiveMistakes == 3:
            text = Text(red, 40)
            text.display(screen, 100, 500, "Game Over")

    def displayGameEnding(self, screen):
        if self.humanScore < self.computerScore:
            text = Text(red, 40)
            text.display(screen, 100, 500, "Game Over")
        elif self.humanScore > self.computerScore:
            text = Text(blue, 40)
            text.display(screen, 100, 500, "You won")
        elif self.humanScore == self.computerScore:
            text = Text(green, 40)
            text.display(screen, 100, 500, "Draw")


class HumanAvailableTimePerTurn():
    def __init__(self, maximumTime, fps):
        self.fps = fps
        self.maximumTime = maximumTime
        self.numbHelper = maximumTime * fps
        self.numbToDisplay = 0

    def decreaseNumbHelper(self):
        self.numbHelper -= 1

    def displayTime(self, screen, screenColor):
        pygame.draw.rect(screen, screenColor, (265, 15, 100, 50))
        text = Text(black, 30)
        text.display(screen, 315, 50, str(self.numbToDisplay))

        if self.numbHelper == 0:
            self.numbHelper = self.fps * self.maximumTime
        elif self.numbHelper % self.fps == 0:
            self.numbToDisplay += 1


if __name__ == '__main__':
    main()
