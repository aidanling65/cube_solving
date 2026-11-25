from cube_lib.cube_utils import pad, parse_algorithm, create_cube, print_cube, shuffle_cube
from cube_lib.cube_strings import simplify
from cube_lib.cube_moves import U, Y
from .yellow_top import yellow_top
from .daisy import daisy
from .cross import cross
from .white_corners import white_corners
from .beginner_utils import U_PREFIX

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
  
  print(alg)
  print_cube(cube)