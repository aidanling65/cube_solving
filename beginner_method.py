from cube_lib.cube_utils import CENTERS,YELLOW_CENTER,EDGES, LAYER_2_EDGES, LAYER_3_EDGES, parse_algorithm, create_cube, shuffle_cube, print_cube
from cube_lib.cube_strings import pad, invert_move, simplify, alg_length
from cube_lib.cube_moves import Y, U
import numpy as np
import time

def yellow_top(cube):
  for i in CENTERS:
    colour = str(cube[i])[0]
    if colour == "2":
      match i:
        case (0,1,1):
          return ""
        case (1,0,1):
          return "X'"
        case (1,1,0):
          return "Z"
        case (1,1,2):
          return "Z'"
        case (1,2,1):
          return "X"
        case (2,1,1):
          return "X2"

def edge_black(cubie, idx):
  if idx == YELLOW_CENTER:
    return cubie
  if idx not in EDGES:
    return 0

  padded = pad(cubie)
  if "1" not in padded:
    return 0
  return int("".join(d if d == "1" else "0" for d in padded))

#assumes yellow top already done
def blackout_edges(cube):
  new_cube = cube.copy()
  for idx in np.ndindex(cube.shape):
    new_cube[idx] = edge_black(cube[idx], idx)
  return new_cube

def white_edge_count(face):
  count = 0
  for i in LAYER_2_EDGES:
    if pad(face[i])[0] == "1":
      count += 1
  return count

class DaisyAlg:
  def __init__(self, alg_str, final_pos):
    self.alg_str = alg_str
    self.final_pos = final_pos


daisy_cases = {
    ((0,0,1), "010") : DaisyAlg("B'UR'",(0,0,1)),
    ((0,1,0), "001") : DaisyAlg("LU'F",(0,1,0)),
    ((0,1,2), "001") : DaisyAlg("R'UF'",(0,1,2)),
    ((0,2,1), "010") : DaisyAlg("FU'R",(0,2,1)),
    ((1,0,0), "010") : DaisyAlg("L",(0,1,0)),
    ((1,0,0), "001") : DaisyAlg("B'",(0,0,1)),
    ((1,0,2), "010") : DaisyAlg("R'",(0,1,2)),
    ((1,0,2), "001") : DaisyAlg("B",(0,0,1)),
    ((1,2,0), "001") : DaisyAlg("F",(0,2,1)),
    ((1,2,0), "010") : DaisyAlg("L'",(0,1,0)),
    ((1,2,2), "001") : DaisyAlg("F'",(0,2,1)),
    ((1,2,2), "010") : DaisyAlg("R",(0,1,2)),
    ((2,0,1), "010") : DaisyAlg("BR",(0,1,2)),
    ((2,0,1), "100") : DaisyAlg("B2",(0,0,1)),
    ((2,1,0), "100") : DaisyAlg("L2",(0,1,0)),
    ((2,1,0), "001") : DaisyAlg("L'F",(0,2,1)),
    ((2,1,2), "100") : DaisyAlg("R2",(0,1,2)),
    ((2,1,2), "001") : DaisyAlg("RF'",(0,2,1)),
    ((2,2,1), "100") : DaisyAlg("F2",(0,2,1)),
    ((2,2,1), "010") : DaisyAlg("F'R",(0,2,1))
}

def daisy(cube):
  sequence = ""

  #isolate edges to only whites
  new_cube = blackout_edges(cube)

  #count number of white edges at top
  white_top_count = white_edge_count(new_cube[0])
  while white_top_count < 4:
    for idx in EDGES:
      move = (idx, pad(new_cube[idx]))
      if move in daisy_cases:
        new_move = daisy_cases[move]
        move_str = new_move.alg_str
        end_pos = new_move.final_pos
        test_cube = new_cube.copy()

        #if move moves another white edge out of the cross, then shift top layer
        u_count = 0
        for _ in range(3):
          if pad(test_cube[end_pos])[0] == "1":
            test_cube = U(test_cube)
            u_count += 1

        #add top layer shifts to algorithm string
        match u_count:
          case 1:
            move_str = "U" + move_str
          case 2:
            move_str = "U2" + move_str
          case 3:
            move_str = "U'" + move_str

        new_cube = parse_algorithm(move_str, new_cube)

        white_top_count = white_edge_count(new_cube[0])
        sequence = sequence + move_str

  print(sequence)
  return sequence

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
  print(sequence)
  return sequence

def white_top_corners(cube):
  count = 0
  top_face = cube[0]
  if "1" in pad(top_face[0,0]):
    count +=1
  if "1" in pad(top_face[0,2]):
    count +=1
  if "1" in pad(top_face[2,0]):
    count +=1
  if "1" in pad(top_face[2,2]):
    count +=1

  return count

CORNER_CENTRES = {
    (0,0,0) : [(0,1,1), (1,0,1), (1,1,0)],
    (0,0,2) : [(0,1,1), (1,0,1), (1,1,2)],
    (0,2,0) : [(0,1,1), (1,1,0), (1,2,1)],
    (0,2,2) : [(0,1,1), (1,1,2), (1,2,1)],
    (2,0,0) : [(1,0,1), (1,1,0), (2,1,1)],
    (2,0,2) : [(1,0,1), (1,1,2), (2,1,1)],
    (2,2,0) : [(1,1,0), (1,2,1), (2,1,1)],
    (2,2,2) : [(1,2,1), (1,1,2), (2,1,1)]
}

def insert_move(corner):
  if corner[0] == "1":
    return "YFRU2R'F'Y'"
  elif corner[1] == "1":
    return "F'U'F"
  else:
    return "RUR'"

def white_corners_top(cube):
  temp_cube = cube.copy()
  sequence = ""

  #check top corners
  corner_pos = (0,2,2)
  edge_1_pos = (2,2,1)
  edge_2_pos = (2,1,2)

  while white_top_corners(temp_cube) > 0:
      edge_1 = pad(temp_cube[edge_1_pos])
      edge_2 = pad(temp_cube[edge_2_pos])

      corner_criteria = set(["1", edge_1[1], edge_2[2]])

      found = False
      new_move = ""

      for i in range(4):
        corner = pad(temp_cube[corner_pos])
        set_corner = set(list(corner))
        if set_corner  == corner_criteria:
          found = True
          break
        else:
          temp_cube = U(temp_cube)
          if i == 0:
            new_move = "U"
          elif i == 1:
            new_move = "U2"
          elif i == 2:
            new_move = "U'"
          else:
            new_move = ""

      sequence = sequence + new_move

      if found:
        new_move = insert_move(corner)

        sequence = sequence + new_move
        temp_cube = parse_algorithm(new_move, temp_cube)

      sequence = sequence + "Y"
      temp_cube = Y(temp_cube)

  return sequence

def is_corner_correct(cube, corner_pos):
  corner = pad(cube[corner_pos])
  edge_1 = pad(cube[corner_pos[0], corner_pos[1], 1])

  if edge_1[1] != corner[1] or edge_1[0] != corner[0]:
    return False

  edge_2 = pad(cube[corner_pos[0], 1, corner_pos[2]])
  if edge_2[0] != corner[0] or edge_2[2] != corner[2]:
    return False

  return True

def pullout_corner(cube, corner):
  temp_cube = cube.copy()
  sequence = ""
  y = ""
  if corner == (2,0,0):
    y = "Y2"
  elif corner == (2,0,2):
    y = "Y"
  elif corner == (2,2,0):
    y = "Y'"
  sequence = sequence + y

  temp_cube = parse_algorithm(sequence, temp_cube)
  new_corner = (2,2,2)
  corner_val = pad(temp_cube[new_corner])
  move = ""
  if corner_val[0] == "1" or corner_val[2] == "1":
    move = "RUR'U'"
  elif corner_val[1] == "1":
    move = "F'U'FU"

  temp_cube = parse_algorithm(move, temp_cube)
  sequence = sequence + move

  insert = white_corners_top(temp_cube)
  sequence = sequence + insert + invert_move(y)

  return sequence

def white_corners(cube):
  temp_cube = cube.copy()
  sequence = white_corners_top(temp_cube)
  temp_cube = parse_algorithm(sequence, temp_cube)

  bottom_corners = [(2,0,0), (2,0,2), (2,2,0), (2,2,2)]
  for i in bottom_corners:
    if not is_corner_correct(temp_cube, i):
      move = pullout_corner(temp_cube, i)
      temp_cube = parse_algorithm(move, temp_cube)
      sequence = sequence + move

  sequence = simplify(sequence)
  print(sequence)
  return sequence

def is_edge_solved(cube, edge_pos):
  edge = pad(cube[edge_pos])
  if edge_pos[0] == 0:
    centre = pad(cube[0,1,1])
    if edge[0] != centre[0]:
      return False

  elif edge_pos[0] == 2:
    centre = pad(cube[2,1,1])
    if edge[0] != centre[0]:
      return False

  if edge_pos[1] == 0:
    centre = pad(cube[1,0,1])
    if edge[1] != centre[1]:
      return False

  elif edge_pos[1] == 2:
    centre= pad(cube[1,2,1])
    if edge[1] != centre[1]:
      return False

  if edge_pos[2] == 0:
    centre = pad(cube[1,1,0])
    if edge[2] != centre[2]:
      return False
  elif edge_pos[2] == 2:
    centre = pad(cube[1,1,2])
    if edge[2] != centre[2]:
      return False

  return True


def is_edges_solved(cube):
  if not is_edge_solved(cube,(1,0,0)):
    return False

  if not is_edge_solved(cube,(1,0,2)):
    return False

  if not is_edge_solved(cube,(1,2,0)):
    return False

  if not is_edge_solved(cube,(1,2,2)):
    return False


  return True

side_edge_pos = [
    (1,0,0),
    (1,0,2),
    (1,2,0),
    (1,2,2)
]

LEFT_ALG = "U'L'ULUFU'F'"
RIGHT_ALG = "URU'R'U'F'UF"
U_PREFIX = ["", "U", "U2", "U'"]

def find_insert(temp_cube):
  for u in range(4):
    edge = pad(temp_cube[0,2,1])
    if edge[1] == pad(temp_cube[1,2,1])[1]:
      if edge[0] == pad(temp_cube[1,1,0])[2]:
        return U_PREFIX[u] + LEFT_ALG
      if edge[0] == pad(temp_cube[1,1,2])[2]:
        return U_PREFIX[u] + RIGHT_ALG

    temp_cube = U(temp_cube)
  return None

def side_edges(cube):
  temp_cube = cube.copy()
  sequence = ""

  def apply(alg):
    nonlocal temp_cube, sequence
    temp_cube = parse_algorithm(alg, temp_cube)
    sequence += alg

  while not is_edges_solved(temp_cube):
    for i in range(4):
      alg = find_insert(temp_cube)
      if alg:
        apply(alg)
        break
      apply("Y")
    else:
        for p in side_edge_pos:
          if is_edge_solved(temp_cube, p):
            continue

          back = (p[1] == 0)
          if back:
            apply("Y2")

          left_slot = (p[2] == 2) if back else (p[2] == 0)
          apply(LEFT_ALG if left_slot else RIGHT_ALG)
          if back:
            apply("Y2")
          break

  sequence = simplify(sequence)
  print(sequence)
  return sequence

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

  print(simplify(sequence))
  return sequence

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
    print(sequence)
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
  print(sequence)
  return simplify(sequence)

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
  print(sequence)
  return sequence

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
  print(sequence)
  return sequence

def solve_cube(org_cube):
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
  print(sequence)
  return sequence

if __name__ == "__main__":
  cube = create_cube()
  cube = shuffle_cube(cube)
  print_cube(cube)
  start = time.time()
  solution = solve_cube(cube)
  end = time.time()
  length = end - start
  cube = parse_algorithm(solution,cube)
  print_cube(cube)
  print(alg_length(solution))
  print(length, " seconds!")
