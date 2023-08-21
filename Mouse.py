import API
from DIRECTIONS import Directions
class Mouse:
    def __init__(self, x, y, direction : Directions) -> None:
        self.x = x
        self.y = y
        self.dir = direction

    def getPosition(self) -> tuple:
        return (self.x, self.y)

    def getDirection(self) -> Directions:
        return self.dir
    
    def turnLeft(self) -> None:
        API.turnLeft()
        self.dir = self.dir.turnLeft()

    def turnRight(self) -> None:
        API.turnRight()
        self.dir = self.dir.turnRight()

    def turnAround(self) -> None:
        self.turnRight()
        self.turnRight()
    
    def moveForward(self) -> None:
        API.moveForward()
        if(self.dir == Directions.NORTH): # ^
          self.y += 1
        if(self.dir == Directions.EAST): # ->
          self.x += 1
        if(self.dir == Directions.SOUTH): # South
          self.y -= 1
        if(self.dir == Directions.WEST): # <-
          self.x -= 1


