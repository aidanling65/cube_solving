import json
import numpy as np
from .CFOP_utils import cfop_key, make_solved_ref, str_to_tuple, Colour, isolate_slot
from cube_lib.cube_utils import pad, parse_algorithm, create_cube, print_cube, shuffle_cube
from cube_lib.cube_strings import simplify
from cube_lib.cube_moves import Y, U
from beginner.beginner_method import yellow_top, daisy, cross
from pathlib import Path

Y_TURNS = [("",""), ("Y","Y'"), ("Y2","Y2"), ("Y'","Y")]
def find_case(cube, d, solved_slots=0,depth=2):

  front = Colour(pad(cube[1, 2, 1])[1])
  right = Colour(pad(cube[1, 1, 2])[2])
  isolated = isolate_slot(cube, front, right, Colour.WHITE)

  pre = ""
  for _ in range(4):
      key = cfop_key(isolated)
      if key in d:
          return pre, d[key]
      isolated = U(isolated)
      pre += "U"

  if depth == 0:
    return None

  for j, (turn, undo) in enumerate(Y_TURNS):
    if j > 3 - solved_slots:
      break
    setup = turn + "RUR'" + undo
    result = find_case(parse_algorithm(setup,cube), d, solved_slots, depth-1)
    if result is not None:
      pre, alg = result
      return setup + pre, alg

  return None

def slot_solved(cube, solved):
    front = Colour(pad(cube[1, 2, 1])[1])
    right = Colour(pad(cube[1, 1, 2])[2])
    return np.array_equal(isolate_slot(cube, front, right, Colour.WHITE), solved)

HERE = Path(__file__).resolve().parent
with open(HERE / "f2l_dict.json") as f:
    f2l_dict = {str_to_tuple(k): v for k, v in json.load(f).items()}

def F2L(cube, solved):

    temp_cube = cube.copy()
    moves = []
    done = set()

    while len(done) < 4:
        turn = ""
        for _ in range(4):
            if not slot_solved(temp_cube, solved):
                break

            done.add((Colour(pad(temp_cube[1, 2, 1])[1]),
                      Colour(pad(temp_cube[1, 1, 2])[2])))
            temp_cube = Y(temp_cube)
            turn += "Y"
        else:
            break

        result = find_case(temp_cube, f2l_dict, solved_slots=len(done))
        if result is None:
          moves.append(turn+"Y")
          temp_cube = Y(temp_cube)
          continue

        pre, alg = result
        move = turn + pre + alg
        temp_cube = parse_algorithm(pre+alg, temp_cube)
        moves.append(move)
    final = simplify(" ".join(moves))
    return final


if __name__ == "__main__":
    cube = create_cube()
    solved = make_solved_ref()

    cube = shuffle_cube(cube)
    print_cube(cube)
    cube = parse_algorithm(yellow_top(cube), cube)
    cube = parse_algorithm(daisy(cube), cube)
    cube = parse_algorithm(cross(cube), cube)
    cube = parse_algorithm(F2L(cube, solved), cube)
    print_cube(cube)
    
