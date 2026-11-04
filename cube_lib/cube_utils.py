import numpy as np
from colorama import Style
from .cube_strings import pad, simplify
from .cube_moves import core_moves, moves
import random

COLOURS = {
  "1":"\033[48;5;255m", #white
  "2":"\033[48;5;226m", #yellow
  "3":"\033[48;5;196m", #red
  "4":"\033[48;5;208m", #orange
  "5":"\033[48;5;21m", #blue
  "6":"\033[48;5;34m", #green
  "0":"\033[48;5;16m", # black
}


def create_cube():
  return np.array([
  [[236, 230, 235],
  [206, 200, 205],
  [246, 240, 245]],

 [[ 36,  30,  35],
  [  6,   0,   5],
  [ 46,  40,  45]], 
 [[136, 130, 135],
  [106, 100, 105],
  [146, 140, 145]]])

cube = create_cube()

def get_at(val,idx):
  return val[idx]

STICKER = "  "
SEP = ""

def colourise(sticker):
    # Return the coloured string rather than printing it
    return f"{COLOURS.get(sticker, '')}{STICKER}{Style.RESET_ALL}"

def face_rows(face):
    return [SEP.join(colourise(s) for s in row) for row in face]

FACE_W = 3 * len(STICKER) + 2 * len(SEP)
GAP = "   "
INDENT = " " * (FACE_W + len(GAP))   # empty slot to the left of U and D

def print_net(top, left, front, right, back, bottom):
    for row in face_rows(top):
        print(INDENT + row)
    print("")

    for rows in zip(face_rows(left), face_rows(front),
                    face_rows(right), face_rows(back)):
        print(GAP.join(rows))

    print("")
    for row in face_rows(bottom):
        print(INDENT + row)

def print_cube(cube):
  vectorized_pad = np.vectorize(pad)
  padded = vectorized_pad(cube)

  #slice cube for faces
  top_face = padded[0]
  bottom_face = padded[2]
  front_face = padded[:,2]
  back_face = padded[:,0]
  left_face = padded[:,:,0]
  right_face = padded[:,:,2]

  #filter for relevant number for face
  vec_get = np.vectorize(get_at, excluded={'idx'})
  top_face = vec_get(top_face,0)
  bottom_face = np.flipud(vec_get(bottom_face,0))
  front_face = vec_get(front_face,1)
  back_face = np.fliplr(vec_get(back_face,1))
  left_face = vec_get(left_face,2)
  right_face = np.fliplr(vec_get(right_face,2))

  #print faces
  print_net(top_face, left_face, front_face, right_face, back_face, bottom_face)

def parse_algorithm(text, cube):
  text = text.replace(" ","")
  text = list(text)
  while len(text) > 0:
      token = text.pop(0)
      if len(text) > 0:
        if text[0] == "'":
          token = token + text.pop(0)

        elif text[0] == "2":
          cube = moves[token](cube)
          text.pop(0)

      cube = moves[token](cube)
  return cube



def shuffle_cube(cube, n_moves=15, seed=0):
  move_list = ""
  random.seed(seed)
  for i in range(n_moves):
    move = random.choice(list(core_moves.keys()))
    move_list = move_list + move
    cube = core_moves[move](cube)

  move_list = simplify(move_list)
  print(move_list)
  return cube

EDGES = [(0,0,1), (0,1,0), (0,1,2), (0,2,1),
         (1,0,0), (1,0,2), (1,2,0), (1,2,2),
         (2,0,1), (2,1,0), (2,1,2), (2,2,1)]

LAYER_3_EDGES = [(0,0,1),(0,1,0),(0,1,2),(0,2,1)]
LAYER_2_EDGES = [(0,1),(1,0),(1,2),(2,1)]

CORNERS = [(0,0,0), (0,0,2), (0,2,0), (0,2,2),
           (2,0,0), (2,0,2), (2,2,0), (2,2,2)]

CENTERS = [(0,1,1), (1,0,1),(1,1,0),(1,1,2),(1,2,1),(2,1,1)]

YELLOW_CENTER = (0,1,1)
