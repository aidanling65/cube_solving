import json
import numpy as np
from pathlib import Path
from .CFOP_utils import Colour, str_to_tuple, cfop_key, make_solved_ref
from .F2L import F2L
from .OLL import OLL
from cube_lib.cube_utils import pad, parse_algorithm, create_cube, print_cube, shuffle_cube
from cube_lib.cube_strings import simplify
from cube_lib.cube_moves import Y, U
from beginner.beginner_method import yellow_top, daisy, cross

front_map = {
    Colour.RED: {Colour.RED : Colour.GREEN, Colour.GREEN : Colour.ORANGE, Colour.BLUE : Colour.RED, Colour.ORANGE: Colour.BLUE, Colour.BLACK : Colour.BLACK, Colour.YELLOW : Colour.YELLOW, Colour.WHITE: Colour.WHITE},
    Colour.BLUE: {Colour.BLUE : Colour.GREEN, Colour.RED : Colour.ORANGE, Colour.GREEN : Colour.BLUE, Colour.ORANGE : Colour.RED, Colour.BLACK : Colour.BLACK, Colour.YELLOW : Colour.YELLOW, Colour.WHITE: Colour.WHITE },
    Colour.GREEN: {Colour.GREEN : Colour.GREEN, Colour.RED : Colour.RED, Colour.BLUE : Colour.BLUE, Colour.ORANGE : Colour.ORANGE, Colour.BLACK : Colour.BLACK, Colour.YELLOW : Colour.YELLOW, Colour.WHITE: Colour.WHITE},
    Colour.ORANGE: {Colour.ORANGE : Colour.GREEN, Colour.GREEN : Colour.RED, Colour.RED : Colour.BLUE, Colour.BLUE : Colour.ORANGE, Colour.BLACK : Colour.BLACK, Colour.YELLOW : Colour.YELLOW, Colour.WHITE: Colour.WHITE}
}

def pll_map_cubie(cubie, map):
  return str([map[Colour(char).value] for char in cubie])

def pll_map(cube):
  front_colour = Colour(pad(cube[1,2,1])[1])
  mapping = front_map[front_colour]
  vec_map = np.vectorize(lambda cubie: int("".join([mapping[Colour(char)].value for char in pad(cubie)])))
  return vec_map(cube)

HERE = Path(__file__).resolve().parent
with open(HERE / "pll_dict.json") as f:
    pll_dict = {str_to_tuple(k): v for k, v in json.load(f).items()}

def PLL(cube):
  seq = ""
  temp = cube.copy()
  for i in range(4):
    for i in range(4):
      key = cfop_key(pll_map(temp))
      if key in pll_dict.keys():
        return simplify(seq + pll_dict[key])
      else:
        seq += "U"
        temp = U(temp)
    seq += "Y"
    temp = Y(temp)
  return ""

if __name__ == "__main__":
    cube = create_cube()
    solved = make_solved_ref()
    print_cube(cube)

    cube = shuffle_cube(cube)
    cube = parse_algorithm(yellow_top(cube), cube)
    cube = parse_algorithm(daisy(cube), cube)
    cube = parse_algorithm(cross(cube), cube)
    cube = parse_algorithm(F2L(cube, solved), cube)
    cube = parse_algorithm(OLL(cube), cube)
    cube = parse_algorithm(PLL(cube), cube)
    print_cube(cube)
    