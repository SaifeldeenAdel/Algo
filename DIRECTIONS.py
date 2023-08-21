from enum import Enum

class Directions(Enum):
    NORTH = "n"
    SOUTH = "s"
    WEST = "w"
    EAST = "e"

    
    def turnLeft(self) -> str:
      return {
          Directions.NORTH: Directions.WEST,
          Directions.EAST: Directions.NORTH,
          Directions.SOUTH: Directions.EAST,
          Directions.WEST: Directions.SOUTH,
      }[self]
    
    def turnRight(self) -> str:
      return {
          Directions.NORTH: Directions.EAST,
          Directions.EAST: Directions.SOUTH,
          Directions.SOUTH: Directions.WEST,
          Directions.WEST: Directions.NORTH,
      }[self]
        
