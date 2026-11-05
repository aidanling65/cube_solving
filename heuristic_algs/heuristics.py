import numpy as np
from enum import Enum
from cube_lib.cube_utils import create_cube
from cube_lib.cube_moves import Y, core_moves

class NumericColour(Enum):
  BLACK = 0
  WHITE = 1
  YELLOW = 2
  RED = 3
  ORANGE = 4
  BLUE = 5
  GREEN = 6

def cube_to_oneshot(cube, n_colours=7):
  digits = np.stack([
      cube // 100 % 10,
      cube // 10 % 10,
      cube % 10], axis=-1)
  return np.eye(n_colours, dtype=int)[digits]

def oneshot_numeric(cube):
  digits = cube.argmax(axis=4)
  return digits[...,0] * 100 + digits[...,1] * 10 + digits[...,2]

solved = cube_to_oneshot(create_cube())
def oneshot_similarity(cube):
  temp_solved = solved.copy()
  max_sim = 0
  for _ in range(4):
    a = temp_solved.ravel().astype(float)
    b = cube.ravel().astype(float)
    cosine  = a @ b / (np.linalg.norm(a,2) * np.linalg.norm(b,2))
    temp_solved = Y(temp_solved)
    if cosine > max_sim:
      max_sim = cosine

  if max_sim == 1:
    return True, max_sim
  return False, max_sim

flattened_solved = solved.flatten()
def stickers_matched(cube):
  flattened = cube.flatten()
  matches = flattened == flattened_solved
  count =  int(np.sum(matches))
  return count == 81, count
"""
prob_vec = np.ones([12])
prob_vec = prob_vec / np.sum(prob_vec)
prob_vec = prob_vec.T

conv_weight = 0.5

def weighted_convolutional_dist(cube, k=6):
    s = state_key(cube)
    if k == 1:
        
    
    d_adj = np.array([ weighted_convolutional_dist(f(cube), k-1) for f in core_moves.values() ]).T
    wcv = conv_weight * weighted_convolutional_dist(cube, k-1) @ s + (1- conv_weight) @ prob_vec @ d_adj
    correct = wcv == 0
    return correct, wcv
"""

def state_key(cube):
  return tuple(cube.flatten().tolist())

def state_key_oneshot(state):
  return np.reshape(np.array(state), (3,3,3,3,7))
  
def state_key_numeric(state):
  return oneshot_numeric(state_key_oneshot(state))

def numeric_state_key(cube):
  return state_key(cube_to_oneshot(cube))
