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
        moveOneCell(maze, mouse, "center")
        log(mouse.getPosition())

    while not maze.backHome(mouse.getPosition()):
        updateWalls(maze, mouse)
        updateFlood(maze, mouse, "home")
        moveOneCell(maze, mouse, "home")
        log(mouse.getPosition())

    maze.setShortestPath()
    followShortestPath(maze, mouse)
    log("Path 1: " + str(len(maze.toCenter)))
    log("Path 2: " + str(len(maze.toHome)))


def updateWalls(maze: Maze, mouse: Mouse) -> None:
    """Updates walls on simulator and maze data"""
    if API.wallFront():
        maze.setWall(mouse.getPosition(), mouse.getDirection())
    if API.wallLeft():
        maze.setWall(mouse.getPosition(), mouse.getDirection().turnLeft())
    if API.wallRight():
        maze.setWall(mouse.getPosition(), mouse.getDirection().turnRight())


def moveOneCell(maze: Maze, mouse: Mouse, flag) -> None:
    """Moves mouse one cell depending on next move"""
    next = getNextCell(maze, mouse)  # Gets next position
    maze.updatePath(next, flag)  # Saves path based on run
    mouse.moveTo(next)  # Moves mouse

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

    # Flood fill algorithm based on if its the center run or home run
    if flag is "center":
        maze.clearFlood("center")
        # Queue starts with all 4 center cells
        queue = [center for center in maze.getCenters()]

        while len(queue) != 0:
            current = queue.pop(0)
            # Goes through all accessible neighbors and updates flood values if they aren't center cells or don't already have a value
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

        # Queue starts with home cell
        queue = [(0, 0)]

        while len(queue) != 0:
            current = queue.pop(0)
            for neighbor in maze.getAccessibleNeighbors(current):
                if (neighbor not in queue) and (not maze.isFlooded(neighbor)):
                    maze.flowFlood(current, neighbor)
                    queue.append(neighbor)

    maze.setFlood()


def followShortestPath(maze: Maze, mouse: Mouse) -> None:
    """Mouse just follows the shortest path stored in the maze"""
    for position in maze.shortestPath:
        mouse.moveTo(position)


if __name__ == "__main__":
    main()
