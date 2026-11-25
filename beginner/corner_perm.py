from cube_lib.cube_utils import pad, parse_algorithm, create_cube, print_cube, shuffle_cube
from cube_lib.cube_strings import simplify
from cube_lib.cube_moves import Y
from .yellow_top import yellow_top
from .daisy import daisy
from .cross import cross
from .white_corners import white_corners
from .second_layer import side_edges
from .yellow_cross import top_cross
from .top_edges import correct_top_edges

def correct_corner_perm(cube):
  corner = pad(cube[0,2,2])
  corner_colours = set(list(corner))
  if str(cube[0,1,1])[0] not in corner_colours:
    return False
  if str(cube[1,2,1])[0] not in corner_colours:
    return False
  if str(cube[1,1,2])[0] not in corner_colours:
    return False

  return True

def corners_correct(cube):
  temp_cube = cube.copy()
  correct_count = 0

  for _ in range(4):
    if correct_count > 1:
      return 4
    correct = correct_corner_perm(temp_cube)
    if correct:
      correct_count += 1

    temp_cube = Y(temp_cube)

  return correct_count


def top_corner_perm(cube):
  temp_cube = cube.copy()
  sequence = ""

  def apply(alg):
    nonlocal temp_cube, sequence
    temp_cube = parse_algorithm(alg, temp_cube)
    sequence += alg

  correct_corner = False

  while not correct_corner:
    for _ in range(4):
        if correct_corner_perm(temp_cube):
          correct_corner = True
          break

        apply("Y")
    if not correct_corner:
      apply("URU'L'UR'U'L")

  for _ in range(3):
    correct_corners = corners_correct(temp_cube)
    if correct_corners == 4:
      break
    elif correct_corners == 1:
      apply("URU'L'UR'U'L")


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
  
  print(alg)
  print_cube(cube)