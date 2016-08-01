import components, engine

class Minesweeper(object):

    def __init__(self):
        self.engine = engine.Engine('Minesweeper', 500, 550)


    def start(self):
        self.grid = components.Grid((10, 10), 10, (0, 50))
        self.grid.createSquares()

        self.engine.addObject(self.grid)
        self.engine.start()



class InfoPanel(engine.GameObject):

    def __init__(self, position, numMines):
        super(InfoPanel, self).__init__(position)

        self.remainingFlags = numMines


    def update(self, objectList, input):
        return



