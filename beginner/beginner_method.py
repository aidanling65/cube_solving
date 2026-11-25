from cube_lib.cube_utils import CENTERS,YELLOW_CENTER,EDGES, LAYER_2_EDGES, LAYER_3_EDGES, parse_algorithm, create_cube, shuffle_cube, print_cube
from cube_lib.cube_strings import pad, invert_move, simplify, alg_length
from cube_lib.cube_moves import Y, U
import numpy as np
import time
from .yellow_top import yellow_top
from .daisy import daisy
from .cross import cross
from .white_corners import white_corners
from .second_layer import side_edges
from .yellow_cross import top_cross
from .top_edges import correct_top_edges
from .corner_perm import top_corner_perm
from .corner_orient import top_corner_orient

def beginner_method(org_cube):
  cube = org_cube.copy()
  sequence = ""

  def apply(alg):
    nonlocal cube, sequence
    cube = parse_algorithm(alg, cube)
    sequence += alg

  apply(yellow_top(cube))
  apply(daisy(cube))
  apply(cross(cube))
  apply(white_corners(cube))
  apply(side_edges(cube))
  apply(top_cross(cube))
  apply(correct_top_edges(cube))
  apply(top_corner_perm(cube))
  apply(top_corner_orient(cube))
  sequence = simplify(sequence)
  return sequence

if __name__ == "__main__":
  cube = create_cube()
  cube = shuffle_cube(cube)
  print_cube(cube)
  start = time.time()
  solution = beginner_method(cube)
  end = time.time()
  length = end - start
  cube = parse_algorithm(solution,cube)
  print_cube(cube)
  print(alg_length(solution))
  print(length, " seconds!")
