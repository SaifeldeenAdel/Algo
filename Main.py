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
    # log(maze.getAccessibleNeighbors(mouse.getPosition()))



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
    if direction == currentDirection.turnLeft():
        mouse.turnLeft()
    elif direction == currentDirection.turnRight():
        mouse.turnRight()
    elif direction != currentDirection:
        mouse.turnAround()
    mouse.moveForward()


def getNextCell(maze: Maze, mouse: Mouse) -> None:
    """Gets next cell position based on lowest neighboring flood array value"""
    position = mouse.getPosition()
    direction = mouse.getDirection()
    neighbors = maze.getAccessibleNeighbors(position)
    for neighbor in neighbors:
        pass
    pass

    maze.clearFlood()


def updateFlood(maze: Maze, mouse: Mouse) -> None:
    """Updates flood array values, runs flood fill algorithm"""
    queue = []
    centers = maze.getCenters()
    for center in centers:
        queue.append(center)

    while len(queue) != 0:
        current = queue.pop(0)
        for neighbor in maze.getAccessibleNeighbors(current):
            if (
                not maze.isInCenter(neighbor)
                and (neighbor not in queue)
                and (not maze.isFlooded(neighbor))
            ):
                maze.flowFlood(current, neighbor)
                queue.append(neighbor)
    log("updated")


if __name__ == "__main__":
    main()
