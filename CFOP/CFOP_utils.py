import json
import numpy as np
import re
import ast
from enum import Enum
from cube_lib.cube_utils import pad, create_cube

class Colour(Enum):
  BLACK='0'
  WHITE='1'
  YELLOW='2'
  RED='3'
  ORANGE='4'
  BLUE='5'
  GREEN='6'

def cfop_key(cube):
    return tuple(cube.ravel())

def cfop_key_cube(key):
    return np.reshape(np.array(key), (3,3,3))

def str_to_tuple(s):
    # "(np.int64(0), np.int64(306), ...)" -> "(0, 306, ...)"
    cleaned = re.sub(r"np\.int64\((-?\d+)\)", r"\1", s)
    return ast.literal_eval(cleaned)

def isolate_slot(cube, front, right, bottom=Colour.WHITE):
  def convert(ch):
    c = Colour(ch)
    if c == bottom: return Colour.WHITE
    if c == front: return Colour.RED
    if c == right: return Colour.GREEN
    return Colour.BLACK

  def relevant(cols):
    return (cols == {bottom, front, right}
      or cols == {front,right}
      or (bottom in cols and len(cols) == 2)
      or cols == {bottom}) or cols == {front} or cols == {right}

  def f(cubie):
    padded = pad(cubie)
    cols = {Colour(c) for c in padded} - {Colour.BLACK}
    if not relevant(cols):
      return 0

    return int("".join(str(convert(c).value) for c in padded))

  return np.vectorize(f, otypes=[int])(cube)

def make_solved_ref():
    c = create_cube()
    front = Colour(pad(c[1, 2, 1])[1])
    right = Colour(pad(c[1, 1, 2])[2])
    return isolate_slot(c, front, right, Colour.WHITE)