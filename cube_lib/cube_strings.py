import re

def pad(num):
  return "{:03d}".format(num)

MOVE_RE = re.compile(r"[A-Za-z](?:2|')?")

def tokenize(sequence):
  return MOVE_RE.findall(sequence)

def move_to_turns(move):
  face = move[0]
  if move.endswith("2"):
    return face, 2
  if move.endswith("'"):
    return face,3
  return face,1

def turns_to_move(face, turns):
  turns %= 4
  if turns == 0:
    return None
  if turns == 1:
    return face
  if turns == 2:
    return face + "2"
  return face + "'"

def simplify(sequence):
  tokens = tokenize(sequence)
  result = []
  for tok in tokens:
    face, turns = move_to_turns(tok)
    if result and result[-1][0] == face:
      _, prev_turns = result[-1]
      combined = prev_turns + turns
      if combined % 4 == 0:
        result.pop()
      else:
        result[-1] = (face, combined % 4)
    else:
      result.append((face,turns))
  return "".join(turns_to_move(f,t) for f,t in result if turns_to_move(f,t))

def invert_move(move):
  if len(move) == 0:
    return move
  elif len(move) == 1:
    return move + "'"
  elif move[1] == "'":
    return move[0]
  else:
    return move
  
def alg_length(text):
  seq = text.replace("'", "").replace("2","")
  return len(seq)