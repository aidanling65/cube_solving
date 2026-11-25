from cube_lib.cube_utils import pad, parse_algorithm, create_cube, print_cube, shuffle_cube
from cube_lib.cube_strings import simplify
from .yellow_top import yellow_top
from .daisy import daisy
from .cross import cross
from .white_corners import white_corners
from .second_layer import side_edges
from .yellow_cross import top_cross
from .top_edges import correct_top_edges
from .corner_perm import top_corner_perm

def is_corner_solved(cube):
  corner = pad(cube[0,2,2])
  return corner[0] == str(cube[0,1,1])[0]

def top_corner_orient(cube):
  temp_cube = cube.copy()
  sequence = ""

  def apply(alg):
    nonlocal temp_cube, sequence
    temp_cube = parse_algorithm(alg, temp_cube)
    sequence += alg

  for _ in range(4):
    for _ in range(4):
      if is_corner_solved(temp_cube):
        break
      apply("R'D'RD")

    apply("U")

  sequence = simplify(sequence)
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
  
  alg = correct_top_edges(cube)
  cube = parse_algorithm(alg, cube)
  
  alg = top_corner_perm(cube)
  cube = parse_algorithm(alg, cube)
  
  alg = top_corner_orient(cube)
  cube = parse_algorithm(alg, cube)
  
  print(alg)
  print_cube(cube)