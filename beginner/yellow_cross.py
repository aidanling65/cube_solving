from cube_lib.cube_utils import pad, parse_algorithm, create_cube, print_cube, shuffle_cube
import numpy as np
from .yellow_top import yellow_top
from .daisy import daisy
from .cross import cross
from .white_corners import white_corners
from .second_layer import side_edges

def top_yellow(cubie):
  return pad(cubie)[0] == "2"

def is_line(top_layer):
  if top_layer.shape != (3,3):
    return False

  return np.array_equal(top_layer[1], [True,True,True])

def is_corner(top_layer):
  if top_layer.shape != (3,3):
    return False

  return top_layer[0,1] and top_layer[1,0]

def is_cross(top_layer):
  if top_layer.shape != (3,3):
    return False

  return (top_layer[0,1] and top_layer[1,0] and top_layer[1,2] and top_layer[2,1])

def is_dot(top_layer):
  return not (top_layer[0,1] or top_layer[1,0] or top_layer[1,2] or top_layer[2,1])


def top_cross(cube):
  vec_top = np.vectorize(top_yellow)

  def apply(alg):
    nonlocal temp_cube, sequence
    temp_cube = parse_algorithm(alg, temp_cube)
    sequence += alg

  temp_cube = cube.copy()

  move = "FRUR'U'F'"
  sequence = ""
  top_layer = vec_top(temp_cube[0])
  while not is_cross(top_layer):
    if is_dot(top_layer) or is_corner(top_layer) or is_line(top_layer):
      apply(move)
    else:
      apply("U")

    top_layer = vec_top(temp_cube[0])

  return sequence

if __name__ == "__main__":
  cube = create_cube()
  cube = shuffle_cube(cube, n_moves=15, seed=69)
  print_cube(cube)
  
  alg = yellow_top(cube)
  cube = parse_algorithm(alg, cube)
  
  alg = daisy(cube)
  cube = parse_algorithm(alg, cube)
  
  alg = cross(cube)
  cube = parse_algorithm(alg, cube)
  
  alg = white_corners(cube)
  cube = parse_algorithm(alg, cube)
  
  alg = side_edges(cube)
  cube = parse_algorithm(alg, cube)  
  
  alg = top_cross(cube)
  cube = parse_algorithm(alg, cube)
  
  print(alg)
  print_cube(cube)