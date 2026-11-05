from enum import Enum
from cube_lib.cube_strings import pad
import numpy as np
from cube_lib.cube_utils import create_cube, print_cube, shuffle_cube, parse_algorithm
from .beginner_method import yellow_top, daisy, cross

class Colour(Enum):
  WHITE = "1"
  YELLOW = "2"
  RED = "3"
  ORANGE = "4"
  BLUE = "5"
  GREEN = "6"
  BLACK = "0"


class PrimaryColour(Enum):
  WHITE = "1"
  RED = "3"
  GREEN = "6"
  BLACK = "0"

def filter_colour(cubie, allowed):
  cols = {Colour(c) for c in pad(cubie)} - {Colour.BLACK}
  if all(col in allowed for col in cols):
    return cubie
  else:
    return 0

def map_colour(cubie, bottom, front, right):
  def convert(ch):
    c = Colour(ch)
    if c == bottom: return PrimaryColour.WHITE
    if c == front: return PrimaryColour.RED
    if c == right: return PrimaryColour.GREEN
    if c == "0": return PrimaryColour.BLACK
    return PrimaryColour.BLACK

  return int("".join(convert(ch).value for ch in pad(cubie)))

"""f2l_dict = {
    np.array([
        [
          [0,0,0],
          [0,0,306],
          [0,0,316]
        ],
          []
        ])
}"""

def F2L(cube):
  temp_cube = cube.copy()
  vec_filter = np.vectorize(filter_colour, excluded={1,'colours'})
  vec_map_colour = np.vectorize(map_colour, excluded={1,'bottom', 2, 'front', 3, 'right'})
  solved = np.array([
  [[ 0, 0, 6],
   [ 0, 0, 6],
   [ 30, 30, 36]],
  [[ 0, 0, 6],
   [ 0, 0, 6],
   [ 30, 30, 36]],
  [[100, 100, 106],
   [100, 100, 106],
   [130, 130, 136]]
  ])
  for i in range(4):
    cols = [
        Colour(pad(temp_cube[1,2,1])[1]),
        Colour(pad(temp_cube[1,1,2])[2]),
        Colour.WHITE, Colour.BLACK
    ]
    temp_cube = vec_filter(cube, cols)
    temp_cube = vec_map_colour(cube, Colour.WHITE, cols[0] , cols[1])
    print(type(temp_cube))
    if np.array_equal(temp_cube,solved):
      continue
    print_cube(temp_cube)
    temp_cube = cube.copy()

if __name__ == "__main__":
  cube = create_cube()
  print_cube(cube)
  F2L(cube)

  cube = shuffle_cube(cube)
  cube = parse_algorithm(yellow_top(cube), cube)
  cube = parse_algorithm(daisy(cube), cube)
  cube = parse_algorithm(cross(cube), cube)
  print_cube(cube)
F2L(cube)
