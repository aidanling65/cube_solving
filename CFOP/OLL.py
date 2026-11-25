import numpy as np
from .CFOP_utils import cfop_key, str_to_tuple, Colour, make_solved_ref
from cube_lib.cube_utils import pad, parse_algorithm, create_cube, print_cube, shuffle_cube
from cube_lib.cube_strings import simplify
from cube_lib.cube_moves import Y
from .F2L import F2L
import beginner.beginner_method as beginner_method
from pathlib import Path
import json

def isolate_oll(cube):
  def convert(ch):
    c = Colour(ch)
    if c == Colour.YELLOW: return c
    return Colour.BLACK

  def f(cubie):
    padded = pad(cubie)
    return int("".join(str(convert(c).value) for c in padded))

  return np.vectorize(f, otypes=[int])(cube)

HERE = Path(__file__).resolve().parent
with open(HERE / "oll_dict.json") as f:
    oll_dict = {str_to_tuple(k): v for k, v in json.load(f).items()}

def OLL(cube):
  oll_isolated = isolate_oll(cube)
  ys = ""
  for _ in range(4):
    if cfop_key(oll_isolated) in oll_dict:
      break
    else:
      oll_isolated = Y(oll_isolated)
      ys += "Y"

  cube=parse_algorithm(simplify(ys), cube)
  key = tuple(int(x) for x in cfop_key(oll_isolated))
  oll_move = oll_dict[key]
  return simplify(ys) + oll_move

if __name__ == "__main__":
    cube = create_cube()
    solved = make_solved_ref()
    print_cube(cube)

    cube = shuffle_cube(cube)
    cube = parse_algorithm(beginner_method.yellow_top(cube), cube)
    cube = parse_algorithm(beginner_method.daisy(cube), cube)
    cube = parse_algorithm(beginner_method.cross(cube), cube)
    cube = parse_algorithm(F2L(cube, solved), cube)
    cube = parse_algorithm(OLL(cube), cube)
    print_cube(cube)