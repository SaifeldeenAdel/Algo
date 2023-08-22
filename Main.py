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
    # maze.setWall((6,7),Directions.EAST)

    while not maze.isInCenter(mouse.getPosition()):
      updateWalls(maze, mouse)
      updateFlood(maze, mouse, "center")
      move(maze, mouse, "center")
      log(mouse.getPosition())

    while not maze.backHome(mouse.getPosition()):
      updateWalls(maze, mouse)
      updateFlood(maze, mouse, "home")
      move(maze, mouse, "home")
      log(mouse.getPosition())

    maze.setShortestPath()



def updateWalls(maze: Maze, mouse: Mouse) -> None:
    """Updates walls on simulator and maze data"""
    if API.wallFront():
        maze.setWall(mouse.getPosition(), mouse.getDirection())
    if API.wallLeft():
        maze.setWall(mouse.getPosition(), mouse.getDirection().turnLeft())
    if API.wallRight():
        maze.setWall(mouse.getPosition(), mouse.getDirection().turnRight())


def move(maze: Maze, mouse: Mouse, flag) -> None:
    """Moves mouse one cell depending on next move"""
    currentX, currentY = mouse.getPosition()
    nextX, nextY = getNextCell(maze, mouse)

    maze.updatePath((nextX, nextY), flag)

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
    maze.setColor(mouse.getPosition())


def getNextCell(maze: Maze, mouse: Mouse) -> None:
    """Gets next cell position based on lowest neighboring flood array value"""
    position = mouse.getPosition()
    neighbors = maze.getAccessibleNeighbors(position)

    minValue = 1000
    minNeighbor = ()
    for neighbor in neighbors:
        if maze.getFloodValue(neighbor) < minValue:
            minValue = maze.getFloodValue(neighbor)
            minNeighbor = neighbor

    return minNeighbor


def updateFlood(maze: Maze, mouse: Mouse, flag: str) -> None:
    """Updates flood array values, runs flood fill algorithm"""

    if flag is "center":
        maze.clearFlood("center")
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

    elif flag is "home":
        maze.clearFlood("home")
        queue = [(0, 0)]

        while len(queue) != 0:
            current = queue.pop(0)
            for neighbor in maze.getAccessibleNeighbors(current):
                if (neighbor not in queue) and (not maze.isFlooded(neighbor)):
                    maze.flowFlood(current, neighbor)
                    queue.append(neighbor)

    maze.setFlood()


if __name__ == "__main__":
    main()
