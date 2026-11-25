import numpy as np

from cube_lib.cube_utils import YELLOW_CENTER, EDGES, LAYER_2_EDGES, pad, parse_algorithm, create_cube, print_cube, shuffle_cube
from cube_lib.cube_moves import U
from .yellow_top import yellow_top


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

  return sequence

if __name__ == "__main__":
  cube = create_cube()
  cube = shuffle_cube(cube, n_moves=15, seed=69)
  print_cube(cube)
  alg = yellow_top(cube)
  cube = parse_algorithm(alg, cube)
  alg = daisy(cube)
  print(alg)
  cube = parse_algorithm(alg, cube)
  print_cube(cube)