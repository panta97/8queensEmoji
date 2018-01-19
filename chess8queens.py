import pygame
import sys
import time
from pygame.locals import *  # like the std in c++

# my classes
from backTracking import Computer, Board
from utils import Text, Helper
from scores import PlayersDetails
from timer import HumanAvailableTimePerTurn
from board import PaintBoardAndQueens, BoardHint
from refresher import GameStateRefresher


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
    gamePainter = PaintBoardAndQueens(screen, color1, color2, colorEdge, squares, size)
    refresher = GameStateRefresher()
    board = Board()
    boardHint = BoardHint(squares, boardPosX, boardPosY, size)
    # this class takes care of the computer and humann scores
    playersDetails = PlayersDetails()
    humanAvailableTimePerTurn = HumanAvailableTimePerTurn(30, FPS)

    gamePainter.paintBoard(boardPosX, boardPosY)
    refresher.displayTextOptions(screen, white)
    # displayTextOptions(screen)

    # mousex = 0
    # mousey = 0
    hintEnable = False
    hintColor = green
    undoMoveEnable = False
    # lastPiecePlaced = None

    # in order to enable the toggle hit feature i'll create the pieces variable
    # pieces = None

    while True:
        # para las teclas que seran presionadas
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                boxx, boxy = helper.getBoxAtPixel(mousex, mousey, squares, size, boardPosX, boardPosY)

                if boxx != None and boxy != None:
                    # if new placed piece is attacking any other queen
                    if board.isAttackingAny((boxx, boxy)):

                        playersDetails.substractPointsToHuman()
                        playersDetails.displayGameOverIfIsThreeConsecutiveMistakes(screen)
                        playersDetails.refreshHumanScore(screen, screenColor)

                    else:
                        gamePainter.paintQueenAt(boxx, boxy)
                        board.PlaceQueen(boxx, boxy)
                        boardHint.changeBoardHintState(boxx, boxy)

                        # gets you the new board

                        computer = Computer()
                        newboard = computer.computerTurn(board)
                        # pieces = board.getPieces() redundant

                        # print(newboard)

                        playersDetails.addPointsToHuman()
                        playersDetails.resetHumanConsecutiveMistakes()
                        playersDetails.refreshHumanScore(screen, screenColor)

                        # reset the timer for the nest hPlayer turn
                        humanAvailableTimePerTurn.resetTimer()
                        # undoTextRefreshColor(screen)
                        # pygame.draw.rect(screen, screenColor, (30, 380, 140, 50))
                        # text = Text(black, 30)
                        # text.display(screen, 100, 400, "undo - U")

                        if newboard is None:
                            print("You Win")

                            playersDetails.displayGameEnding(screen)

                        else:

                            newQueenPosition = helper.boardDistinc(board.getBoard(), newboard, squares)
                            # el boardDistinc te devuelve la posicion donde se pueso la nueva pieza
                            boxx, boxy = newQueenPosition

                            # displayEmoji(screen, "thinking")
                            refresher.displayEmoji(screen, "thinking", screenColor)
                            gamePainter.paintQueenAt(boxx, boxy)
                            # displayEmoji(screen, "smiling")
                            refresher.displayEmoji(screen, "smiling", screenColor)

                            board.PlaceQueen(boxx, boxy)
                            boardHint.changeBoardHintState(boxx, boxy)

                            # pieces = board.getPieces() redundant
                            print(board.getPieces())
                            # print(newQueenPosition)

                            lastPiecePlaced = (boxx, boxy)

                            # para deshacer la jugada una vez por turno
                            if undoMoveEnable is False:
                                undoMoveEnable = True

                            playersDetails.addPointsToComputer()
                            playersDetails.refreshComputerScore(screen, screenColor)

                # necesitas este hint tambien para mostrar las pistas despues de volverlas a activarlas
                if hintEnable == True:
                    boardHint.drawHints(screen, hintColor)

                if boardHint.getAvailableSpaces() == 0:
                    playersDetails.displayGameEnding(screen)

                print("look here")
                print(boardHint.getAvailableSpaces())

            # TOGGLE HINT
            if pressed[pygame.K_h]:
                hintEnable = helper.toggleVal(hintEnable)
                if hintEnable == True:
                    boardHint.drawHints(screen, hintColor)
                else:
                    # pieces = board.getPieces()

                    if board.getPieces() is None:
                        continue
                    gamePainter.paintBoard(boardPosX, boardPosY)
                    # pieces significa la posiciones donde estan las reynas
                    gamePainter.repaintQueens(board.getPieces())

                    # for piece in (pieces):
                    #     drawBoard.drawQueenAt(piece[0], piece[1], screen)
                    # print(piece[0])

            # RESTART GAME
            if pressed[pygame.K_r]:
                # print("you have to restart the game")
                # print(board)
                board.restarBoard()
                boardHint.restart()
                pieces = None

                # print(board)
                playersDetails.resetScores()
                playersDetails.refreshHumanScore(screen, screenColor)
                playersDetails.refreshComputerScore(screen, screenColor)
                gamePainter.paintBoard(boardPosX, boardPosY)

                humanAvailableTimePerTurn.resetTimer()

            # UNDO MOVE'S OPPONENT
            if pressed[pygame.K_u]:
                if undoMoveEnable:
                    board.RemoveQueen(lastPiecePlaced[0], lastPiecePlaced[1])

                    print(board.pieces)
                    print(lastPiecePlaced[0], lastPiecePlaced[1])

                    gamePainter.paintBoard(boardPosX, boardPosY)
                    gamePainter.repaintQueens(board.getPieces())
                    # for piece in (board.pieces):
                    #     gamePainter.paintQueenAt(piece[0], piece[1])

                    pygame.draw.rect(screen, screenColor, (30, 380, 140, 50))

                    refresher.disableUndoText(screen, gray, screenColor)

                    boardHint.changeBoardHintStateInverse(board.getPieces())

                    if hintEnable:
                        boardHint.drawHints(screen, hintColor)

                    undoMoveEnable = helper.toggleVal(undoMoveEnable)

                # print(pieces)
                # print(board.pieces)

        humanAvailableTimePerTurn.decreaseNumbHelper()
        humanAvailableTimePerTurn.displayTime(screen, screenColor)
        humanAvailableTimePerTurn.isTimeZero(screen)

        fpsClock.tick(FPS)
        pygame.display.update()


if __name__ == '__main__':
    main()
