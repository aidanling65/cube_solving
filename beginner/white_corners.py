from cube_lib.cube_utils import pad, parse_algorithm, create_cube, print_cube, shuffle_cube
from cube_lib.cube_moves import U, Y
from cube_lib.cube_strings import simplify, invert_move
from .yellow_top import yellow_top
from .daisy import daisy
from .cross import cross

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
  
  print(alg)
  print_cube(cube)