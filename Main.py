import API
import sys
from Maze import Maze
from Mouse import Mouse
from DIRECTIONS import Directions


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


def main():
    log("Running...")
    API.setColor(0, 0, "G")
    API.setText(0, 0, "START")

    maze = Maze(API.mazeWidth(), API.mazeHeight())
    mouse = Mouse(0, 0, Directions.NORTH)

    while not maze.isInCenter(mouse.getPosition()):
        updateWalls(maze, mouse)
        updateFlood(maze, mouse)
        getNextCell(maze, mouse)
        move(maze, mouse)

def updateWalls(maze: Maze, mouse: Mouse) -> None:
    """Updates walls on simulator and maze data"""
    if API.wallFront():
        maze.setWall(mouse.getPosition(), mouse.getDirection())
    if API.wallLeft():
        maze.setWall(mouse.getPosition(), mouse.getDirection().turnLeft())
    if API.wallRight():
        maze.setWall(mouse.getPosition(), mouse.getDirection().turnRight())


def move(maze: Maze, mouse: Mouse) -> None:
    """Moves mouse one cell depending on next move"""
    currentX, currentY = mouse.getPosition()
    nextX, nextY = getNextCell(maze, mouse)
    if nextX < currentX:
        direction = Directions.WEST
    elif nextX > currentX:
        direction = Directions.EAST
    elif nextY < currentY:
        direction = Directions.SOUTH
    elif nextY > currentY:
        direction = Directions.NORTH
    
    currentDirection = mouse.getDirection()
    if(direction == currentDirection.turnLeft()):
        mouse.turnLeft()
    elif(direction == currentDirection.turnRight()):
        mouse.turnRight()
    elif(direction != currentDirection):
        mouse.turnAround()
    mouse.moveForward()


def getNextCell(maze: Maze, mouse: Mouse) -> None:
    """Gets next cell position we need to move to based on flood array values"""
    pass

def updateFlood(maze: Maze, mouse: Mouse) -> None:
    """Updates flood array values, runs flood fill algorithm"""
    maze.clearFlood()
    pass


if __name__ == "__main__":
    main()
