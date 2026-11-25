from cube_lib.cube_utils import pad, parse_algorithm, create_cube, print_cube, shuffle_cube
from cube_lib.cube_strings import simplify
from cube_lib.cube_moves import Y
from .yellow_top import yellow_top
from .daisy import daisy
from .cross import cross
from .white_corners import white_corners
from .second_layer import side_edges
from .yellow_cross import top_cross
from .beginner_utils import U_PREFIX

def incorrect_top_edges(cube):
  temp_cube = cube.copy()
  front_edge = (0,2,1)
  centre_pos = (1,2,1)
  edges = []

  top_edges = [(0,2,1), (0,1,2), (0,0,1), (0,1,0)]
  for i in range(4):
    edge = pad(temp_cube[front_edge])
    centre = pad(temp_cube[centre_pos])
    if edge[1] != centre[1]:
      edges.append(top_edges[i])

    temp_cube = Y(temp_cube)

  return edges

def is_adj_top_edge(edge_1, edge_2):
  match edge_1:
    case (0,0,1):
      if edge_2 == (0,1,0):
        return (True, edge_2)
      elif edge_2 == (0,1,2):
        return (True,edge_1)
      elif edge_2 == (0,2,1):
        return (False, edge_2)
    case (0,1,0):
      if edge_2 == (0,0,1):
        return (True, edge_1)
      elif edge_2 == (0,2,1):
        return (True, edge_2)
      elif edge_2 == (0,1,2):
        return (False, edge_2)
    case (0,1,2):
      if edge_2 == (0,0,1):
        return (True, edge_2)
      elif edge_2 == (0,2,1):
        return (True, edge_1)
      elif edge_2 == (0,1,0):
        return (False, edge_1)
    case (0,2,1):
      if edge_2 == (0,1,0):
        return (True, edge_1)
      elif edge_2 == (0,1,2):
        return (True, edge_2)
      elif edge_2 == (0,0,1):
        return (False, edge_1)

  return (None, None)


swap_move = "RUR'URU2R'U"
def three_edges(cube):
  correct_back_centre = str(cube[1,0,1])
  if correct_back_centre == pad(cube[0,1,0])[1]:
    print("clockwise")
    return "Y'" + swap_move + "Y" + swap_move

  elif correct_back_centre == pad(cube[0,2,1]):
    print("anticlockwise")
    return swap_move + "Y'" + swap_move + "Y"

def correct_top_edges(cube):
  temp_cube = cube.copy()
  sequence = ""

  def apply(alg):
    nonlocal temp_cube, sequence
    temp_cube = parse_algorithm(alg, temp_cube)
    sequence += alg

  incorrect_edges = None
  U_count = ""
  for i in range(4):
    new_edges = incorrect_top_edges(temp_cube)
    if incorrect_edges == None:
      incorrect_edges = new_edges
      U_count = U_PREFIX[i]
    elif len(new_edges) == 0:
      U_count = U_PREFIX[i]
      return sequence
    elif len(new_edges) < len(incorrect_edges):
      U_count = U_PREFIX[i]
      incorrect_edges = new_edges
    apply("U")

  apply(U_count)

  if len(incorrect_edges) == 0:
    sequence = simplify(sequence)
    return sequence
  elif len(incorrect_edges) == 2:
    adj, front = is_adj_top_edge(incorrect_edges[0], incorrect_edges[1])
    match front:
      case (0,1,0):
        apply("Y'")
      case (0,1,2):
        apply("Y")
      case (0,0,1):
        apply("Y2")

    if adj:
      apply(swap_move)
    else:
      apply(swap_move + "Y'" + swap_move + "Y" + swap_move)

  sequence = simplify(sequence)
  return simplify(sequence)

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
  
  print(alg)
  print_cube(cube)