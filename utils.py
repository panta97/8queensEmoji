import pygame


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


class Helper():
    # def __init__(self):

    def leftTopCoordOfSquare(self, x, y, size, boardPosX, boardPosY):
        left = x * size + boardPosX
        top = y * size + boardPosY
        return (left, top)

    def getBoxAtPixel(self, x, y, squares, size, boardPosX, boardPosY):
        for i in range(squares):
            for j in range(squares):
                left, top = self.leftTopCoordOfSquare(i, j, size, boardPosX, boardPosY)
                rect = pygame.Rect(left, top, size, size)
                if rect.collidepoint(x, y):
                    return(i, j)
        return(None, None)

    def toggleVal(self, value):
        if value is True:
            return False
        else:
            return True

    def boardDistinc(self, currentBoard, newBoard, squares):
        for j in range(squares):
            for i in range(squares):
                if currentBoard[j][i] != newBoard[j][i]:
                    return (j, i)
