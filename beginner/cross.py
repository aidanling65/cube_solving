from cube_lib.cube_utils import pad, parse_algorithm, LAYER_3_EDGES, create_cube, print_cube, shuffle_cube
from cube_lib.cube_moves import U
from .yellow_top import yellow_top
from .daisy import white_edge_count, daisy

def get_adj_centre(pos):
  match pos:
    case (0,0,1):
      return (1,0,1)
    case (0,1,0):
      return (1,1,0)
    case (0,1,2):
      return (1,1,2)
    case (0,2,1):
      return (1,2,1)

def get_edge_colour(cube, pos):
  padded = pad(cube[pos])
  if padded[1] == "0":
    return int(padded[2])
  else:
    return int(padded[1])

def get_top_colour(cube, pos):
  padded = pad(cube[pos])
  return int(padded[0])

def get_centre_colour(cube, pos):
  return int(str(cube[pos])[0])

def shift_tile(centre_pos):
  match centre_pos:
    case (1,0,1):
      return "B2"
    case (1,1,0):
      return "L2"
    case (1,1,2):
      return "R2"
    case (1,2,1):
      return "F2"

#only pass cube with  daisy applied
def cross(cube):
  sequence = ""
  test_cube = cube.copy()
  while white_edge_count(test_cube[2]) < 4:
    for edge in LAYER_3_EDGES:
      top_colour = get_top_colour(test_cube, edge)
      if top_colour != 1:
        continue
      edge_colour = get_edge_colour(test_cube,edge)

      centre_pos = get_adj_centre(edge)
      centre_colour = get_centre_colour(test_cube, centre_pos)

      if edge_colour == centre_colour:
          move = shift_tile(centre_pos)
          test_cube = parse_algorithm(move, test_cube)
          sequence = sequence + move
    if white_edge_count(test_cube[2]) < 4:
      test_cube = U(test_cube)
      if len(sequence) > 0:
        if sequence[-1] == "U":
          sequence = sequence + "2"
        elif sequence[-2:] == "U2":
          sequence = sequence[:-1] + "'"
        else:
          sequence = sequence + "U"
      else:
        sequence = sequence + "U"
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
  print(alg)
  cube = parse_algorithm(alg, cube)
  print_cube(cube)