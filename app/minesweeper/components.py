import engine, random

print('start of components')

# Constants
SIZE = 50
VALUE_TO_DISPLAY = {
    -1: 'X',
    0: ''
}
# SQUARE_FONT = engine.createFont('Helvetica')


class Square(engine.GameObject):

    """Properties
        value: the numeric value of the square (-1: mine, 0-8: num of mines surrounding)
        display: the string value shown when square is pressed
        state: enumeration denoting the state the square is currently in
    """

    # state constants
    UNMARKED = 0
    FLAGGED = 1
    QUESTIONED = 2
    PRESSED = 3


    def __init__(self, position, offset, value=0, display=''):
        scaledPos = (position[0] * SIZE + offset[0], position[1] * SIZE + offset[1])
        super(Square, self).__init__(scaledPos)

        self.value = value
        self.display = display
        self.state = Square.UNMARKED
        self.dimension = (SIZE, SIZE)

    def setValue(self, value):
        self.value = value


    def setMine(self):
        self.value = -1


    def click(self):
        self.display = VALUE_TO_DISPLAY.get(self.value, str(self.value))
        self.state = Square.PRESSED
        return self.value


    def cycleMarking(self):
        if self.isUnmarked():
            self.state = Square.FLAGGED
            self.display = ' >'
        elif self.isFlagged():
            self.state = Square.QUESTIONED
            self.display = ' ?'
        elif self.isQuestioned():
            self.state = Square.UNMARKED
            self.display = ''


    def hasMine(self):
        return self.value == -1


    def isEmpty(self):
        return self.value == 0


    def isUnmarked(self):
        return self.state == Square.UNMARKED


    def isPressed(self):
        return self.state == Square.PRESSED


    def isFlagged(self):
        return self.state == Square.FLAGGED


    def isQuestioned(self):
        return self.state == Square.QUESTIONED


    def update(self, objectList, input):
        return


    def draw(self, renderer):
        bgColor = engine.LIGHT_GRAY
        borderColor = engine.DARK_GRAY
        fontColor = engine.BLACK

        if self.isPressed():
            bgColor = engine.NEAR_WHITE
            borderColor = engine.LIGHT_GRAY

            if self.hasMine():
                fontColor = engine.RED

        elif self.isFlagged():
            fontColor = engine.RED

        renderer.fillRect(self.position, self.dimension, bgColor)
        renderer.drawRect(self.position, self.dimension, borderColor)
        renderer.drawText(self.display, self.position, fontColor)



class Grid(engine.GameObject):

    def __init__(self, dimensions, numMines, position=(0,0)):
        super(Grid, self).__init__(position)

        self.width = dimensions[0]
        self.height = dimensions[1]
        self.numMines = numMines
        self.numFlags = 0
        self.neighborOffsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        self.grid = [[]]


    def __createMines(self):
        for n in range(0, self.numMines):
            while True:
                randX = random.randint(0, self.width - 1)
                randY = random.randint(0, self.height - 1)
                square = self.grid[randX][randY]

                if not square.hasMine():
                    square.setMine()
                    break


    def __createNumbers(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                square = self.grid[i][j]
                if not square.hasMine():
                    count = self.__countSurroundingMines(j, i)
                    square.setValue(count)



    def __countSurroundingMines(self, squareX, squareY):
        count = 0
        for offset in self.neighborOffsets:
            x = squareX - offset[0]
            y = squareY - offset[1]

            if 0 <= x < self.width and 0 <= y < self.height:
                square = self.grid[y][x]
                if square != None and square.hasMine():
                    count += 1

        return count


    def createSquares(self):
        for i in range(0, self.height):
            self.grid.append([])
            for j in range(0, self.width):
                self.grid[i].append(Square((j, i), self.position))

        self.__createMines()
        self.__createNumbers()


    def update(self, objectList, input):
        mousePos = input.getMousePos()
        j = (mousePos[0] - self.position[0]) / SIZE
        i = (mousePos[1] - self.position[1]) / SIZE

        if 0 <= j < self.width and 0 <= i < self.height:
            square = self.grid[i][j]
            if input.isMouseLeftReleased():
                self.__recursiveClickSquares(i, j)
                if square.isPressed():
                    self.__clearIfProperlyFlagged(i, j)

            elif input.isMouseRightReleased() and not square.isPressed():
                square.cycleMarking()
                if square.isFlagged():
                    self.numFlags += 1
                elif square.isQuestioned():
                    self.numFlags -= 1


    def draw(self, renderer):
        for arr in self.grid:
            for square in arr:
                square.draw(renderer)


    def __recursiveClickSquares(self, i, j):
        square = self.grid[i][j]
        if square.isUnmarked():
            square.click()

            if square.isEmpty():
                self.__clickSurroundingSquares(i, j)
            elif square.hasMine():
                self.__clickAllMines()


    def __clickSurroundingSquares(self, i, j):
        for offset in self.neighborOffsets:
            x = j - offset[0]
            y = i - offset[1]

            if 0 <= x < self.width and 0 <= y < self.height:
                self.__recursiveClickSquares(y, x)


    def __clearIfProperlyFlagged(self, i, j):
        numFlags = 0
        square = self.grid[i][j]
        for offset in self.neighborOffsets:
            x = j - offset[0]
            y = i - offset[1]

            if 0 <= x < self.width and 0 <= y < self.height:
                if self.grid[y][x].isFlagged():
                    numFlags += 1

        if numFlags == square.value:
            self.__clickSurroundingSquares(i, j)

    def __clickAllMines(self):
        for arr in self.grid:
            for square in arr:
                if square.hasMine():
                    square.click()

        # todo: handle game over...