import pygame, abc, os.path

# Constants

# Colors
BLACK       = (0, 0, 0)
WHITE       = (255, 255, 255)
RED         = (255, 0 ,0)
GREEN       = (0, 255, 0)
BLUE        = (0, 0, 255)
YELLOW      = (255, 255, 0)

NEAR_WHITE  = (225, 225, 225)
LIGHT_GRAY  = (200, 200, 200)
MID_GRAY    = (150, 150, 150)
DARK_GRAY   = (100, 100, 100)



class Engine(object):

    def __init__(self, appName, displayWidth=500, displayHeight=500, frameRate=60, resourcePath='../../resources', defaultFontName='Raleway-Light'):
        self.appName = appName
        self.frameRate = frameRate
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight
        self.resourcePath = resourcePath
        self.defaultFontName = defaultFontName
        self.objectList = []


    def __updateObjects(self, input):
        for obj in self.objectList:
            obj.update(self.objectList, input)


    def __renderObjects(self, renderer):
        for obj in self.objectList:
            obj.draw(renderer)


    def start(self):
        pygame.init()
        surface = pygame.display.set_mode((self.displayWidth, self.displayHeight))
        pygame.display.set_caption(self.appName)

        clock = pygame.time.Clock()
        renderer = Renderer(surface, self.createFont(self.defaultFontName, 30))
        input = Input()

        hasQuit = False
        while not hasQuit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    hasQuit = True

            input.updateInput()
            self.__updateObjects(input)
            self.__renderObjects(renderer)

            pygame.display.flip()
            clock.tick(self.frameRate)

        pygame.quit()
        quit()


    def addObject(self, obj):
        self.objectList.append(obj)

    def createFont(self, name, size=12):
        fileName = os.path.join(os.path.dirname(__file__), self.resourcePath + '/fonts/' + name + '.ttf')
        return pygame.font.Font(fileName, size)



class GameObject(object):

    def __init__(self, position=(0,0)):
        self.position = position


    def getPosition(self):
        return self.position


    @abc.abstractmethod
    def update(self, objectList, input):
        # Handle interactions with other objects here
        return


    @abc.abstractmethod
    def draw(self, renderer):
        # Handle drawing self here
        return



class Renderer(object):

    def __init__(self, surface, defaultFont):
        self.surface = surface
        self.defaultFont = defaultFont


    def drawRect(self, position, dimensions, color=BLACK, thickness=1):
        rect = position + dimensions
        pygame.draw.rect(self.surface, color, rect, thickness)


    def fillRect(self, position, dimensions, color=BLACK):
        rect = position + dimensions
        self.surface.fill(color, rect)


    def drawText(self, text, position, color=BLACK, font=None):
        if font is None:
            font = self.defaultFont

        ren = font.render(text, 0, color)
        self.surface.blit(ren, position)


class Input(object):

    def __init__(self):
        self.prevMouse = (0,0,0)
        self.curMouse = (0,0,0)


    def updateInput(self):
        self.prevMouse = self.curMouse
        self.curMouse = pygame.mouse.get_pressed()

        # do the same for keys as well...


    def isMouseLeftDown(self):
        return self.__isMouseDown(0)


    def isMouseLeftReleased(self):
        return self.__isMouseReleased(0)


    def isMouseRightDown(self):
        return self.__isMouseDown(2)


    def isMouseRightReleased(self):
        return self.__isMouseReleased(2)


    def __isMouseDown(self, index):
        value = self.curMouse[index]
        return (value == 1)


    def __isMouseReleased(self, index):
        value = self.curMouse[index]
        preValue = self.prevMouse[index]
        return (value == 0 and preValue == 1)


    def getMousePos(self):
        return pygame.mouse.get_pos()


    def getKeyTyped(self):
        return pygame.key.get_pressed()