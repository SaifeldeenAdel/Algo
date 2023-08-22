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

    def moveTo(self, nextPosition)->None:
        # Determine next direction
        currentX, currentY = self.x, self.y
        nextX, nextY = nextPosition
        direction = None
        
        if nextX < currentX:
            direction = Directions.WEST
        elif nextX > currentX:
            direction = Directions.EAST
        elif nextY < currentY:
            direction = Directions.SOUTH
        elif nextY > currentY:
            direction = Directions.NORTH

        # Determine where the mouse turns
        currentDirection = self.getDirection()
        if direction == currentDirection.turnLeft():
            self.turnLeft()
        elif direction == currentDirection.turnRight():
            self.turnRight()
        elif direction != currentDirection:
            self.turnAround()
        
        # Moves forward to next cell and sets color on simulator
        self.moveForward()



