import API
from DIRECTIONS import Directions
import sys


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


class Maze:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

        positions = [(j, i) for j in range(width) for i in range(height)]
        self.walls = {position: set() for position in positions}

        # Setting bounding walls
        for position in self.walls:
            x, y = position
            if x == 0:
                self.setWall(position, Directions.WEST)
            if y == 0:
                self.setWall(position, Directions.SOUTH)
            if x == width - 1:
                self.setWall(position, Directions.EAST)
            if y == height - 1:
                self.setWall(position, Directions.NORTH)

        # Setting center squares
        x = width // 2
        y = height // 2
        self.center = set()
        self.center.add((x, y))

        if width % 2 == 0:
            self.center.add((x - 1, y))
        if height % 2 == 0:
            self.center.add((x, y - 1))
        if width % 2 == 0 and height % 2 == 0:
            self.center.add((x - 1, y - 1))

        # Clearing flood, sets all cells to None except center
        self.clearFlood()

        # Draw flood values
        self.setFlood()

    def isInCenter(self, position) -> bool:
        """Checks if mouse is in the center"""
        return position in self.center

    def isValidPosition(self, position):
        x, y = position
        if x >= 0 and y >= 0 and x < self.width and y < self.height:
            return True
        else:
            return False

    def getCenters(self):
        return self.center

    def checkWall(self, position, direction) -> bool:
        """Checks if theres a wall in the direction and position given"""
        return direction in self.walls[position]

    def getAccessibleNeighbors(self, position) -> set:
        """Gets neighboring cells to given position that can be accessed i.e there's no wall in between"""
        x, y = position
        neighbors = set()
        left = (x - 1, y)
        right = (x + 1, y)
        top = (x, y + 1)
        bottom = (x, y - 1)

        if self.isValidPosition(top):
          if Directions.NORTH not in self.walls[position]:
            neighbors.add(top)
        if self.isValidPosition(bottom):
          if Directions.SOUTH not in self.walls[position]:
            neighbors.add(bottom)
        if self.isValidPosition(left):
          if Directions.WEST not in self.walls[position]:
            neighbors.add(left)
        if self.isValidPosition(right):
          if Directions.EAST not in self.walls[position]:
            neighbors.add(right)
        return neighbors

    def clearFlood(self):
        """Sets all flood array cells to blank state (None) except center is set to 0"""
        self.flood = [
            [(None if not self.isInCenter((j, i)) else 0) for j in range(self.width)]
            for i in range(self.height)
        ]

    def flowFlood(self, current, neighbor):
        """Updates flood value"""
        currentX, currentY = current
        neighborX, neighborY = neighbor
        self.flood[neighborX][neighborY] = self.flood[currentX][currentY] + 1
        API.setText(neighborX, neighborY, self.flood[neighborX][neighborY])
        log("hey!")
    
    def isFlooded(self, position):
        """Boolean for if the position already has a flood value or not"""
        x,y = position
        return self.flood[x][y] is not None

    def setWall(self, position, direction):
        """Draws wall on simulator"""
        x, y = position
        self.walls[position].add(direction)
        API.setWall(x, y, direction.value)

    # Draw flood values on map
    def setFlood(self):
        """Draws flood values on simulator"""
        for position in self.walls:
            x, y = position
            API.setText(x, y, self.flood[x][y])
