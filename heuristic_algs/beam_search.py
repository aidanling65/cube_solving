from cube_lib.cube_utils import core_moves
from .heuristics import cube_to_oneshot, state_key
import heapq

def beam_search(cube, h, k=3, max_depth=50, seq=""):
  is_solved, score = h(cube_to_oneshot(cube))
  if is_solved:
    return "", cube

  beam = [(score, [], cube)]
  visited = {state_key(cube)}
  best = beam[0]

  for _ in range(max_depth):
    candidates = []
    for _, moves_so_far, state in beam:
      for name, move_fn in core_moves.items():
          if moves_so_far and name[0] == moves_so_far[-1][0]:
            continue

          next = move_fn(state.copy())
          key = state_key(next)
          if key in visited:
            continue
          visited.add(key)

          solved, sim = h(cube_to_oneshot(next))
          seq = "".join(moves_so_far) + name
          if solved:
            print("Solved!", "".join(seq))
            return seq, next

          candidates.append((sim,seq, next))

    if not candidates:
      break

    beam = heapq.nlargest(k, candidates, key = lambda c: c[0])
    if beam[0][0] < best[0]:
      best = beam[0]

  print("not solved, best score:", best[0])
  return "".join(best[1]),best[2]