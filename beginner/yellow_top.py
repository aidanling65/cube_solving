from cube_lib.cube_utils import CENTERS, create_cube, print_cube, parse_algorithm, shuffle_cube

def yellow_top(cube):
  for i in CENTERS:
    colour = str(cube[i])[0]
    if colour == "2":
      match i:
        case (0,1,1):
          return ""
        case (1,0,1):
          return "X'"
        case (1,1,0):
          return "Z"
        case (1,1,2):
          return "Z'"
        case (1,2,1):
          return "X"
        case (2,1,1):
          return "X2"

if __name__ == "__main__":
    cube = create_cube()
    cube = shuffle_cube(cube, n_moves=15, seed=69)
    print_cube(cube)
    alg = yellow_top(cube)
    print(alg)
    print_cube(parse_algorithm(alg, cube))
