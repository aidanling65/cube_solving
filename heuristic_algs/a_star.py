from .heuristics import state_key, cube_to_oneshot, oneshot_similarity, weighted_convolutional_dist
from cube_lib.cube_utils import create_cube, core_moves, shuffle_cube
import time

class AStarCube():
  def __init__(self, key, g, weight, h, cube, parent=None, move = ""):
    self.key = key
    self.g = g
    self.h = h
    self.cube = cube
    self.f = self.g - weight * self.h
    self.parent = parent
    self.move = move

solved_key = state_key(cube_to_oneshot(create_cube()))

def reconstruct_path(current):
  path = []
  moves = ""
  while current != None:
    path.insert(0,current)
    moves = current.move + moves
    current = current.parent
  return moves

def A_star(cube, weight, h):
  oneshot_cube = cube_to_oneshot(cube)
  start = AStarCube(state_key(oneshot_cube), 0, weight, h(oneshot_cube)[1], cube.copy(), None, "")

  open = {state_key(oneshot_cube) : start}
  closed = set()

  while len(open) > 0:
    current_key, current_val = min(open.items(), key= lambda x: x[1].f)
    if current_key == solved_key:
      return reconstruct_path(current_val)
      
    del open[current_key]
    closed.add(current_key)
    
    print(len(open.keys()),current_val.f )
    for move in core_moves.keys():
      neighbour_cube = core_moves[move](current_val.cube.copy())
      neighbour_oneshot = cube_to_oneshot(neighbour_cube)
      neighbour_state = state_key(neighbour_oneshot)
      
      if neighbour_state in closed:
        continue
      
      neighbour = AStarCube(neighbour_state, current_val.g+1, weight, h(neighbour_oneshot)[1], neighbour_cube, current_val, move)
      tent_g = current_val.g + 1
      
      if neighbour_state not in open:
        open[neighbour_state] = neighbour
      elif tent_g >= open[neighbour_state].g:
        continue
        
      open[neighbour_state] = neighbour
  
  return "Failed"

i=5
weight = 3
cube = create_cube()
cube = shuffle_cube(cube, i)
start_time = time.time()
solution = A_star(cube, weight, weighted_convolutional_dist)
end_time = time.time()
print(f"Scramble length {i}: Solution {solution} found in {end_time-start_time} seconds")


