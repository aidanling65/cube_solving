from cube_lib.cube_utils import pad, parse_algorithm, create_cube, print_cube, shuffle_cube
from cube_lib.cube_strings import simplify
from .CFOP_utils import make_solved_ref
from beginner.beginner_method import yellow_top, daisy, cross
from .F2L import F2L
from .OLL import OLL
from .PLL import PLL



def CFOP_solve(cube):
    yellow_move = yellow_top(cube)
    cube = parse_algorithm(yellow_move, cube)

    daisy_move = daisy(cube)
    cube = parse_algorithm(daisy_move, cube)

    cross_move = cross(cube)
    cube = parse_algorithm(cross_move, cube)
    
    solved = make_solved_ref() 
    f2l_moves = F2L(cube, solved)
    cube = parse_algorithm(f2l_moves, cube)
    
    oll_moves = OLL(cube)
    cube = parse_algorithm(oll_moves, cube)
    
    pll_moves = PLL(cube)
    cube = parse_algorithm(pll_moves, cube)
    
    return simplify(yellow_move + daisy_move + cross_move + f2l_moves + oll_moves + pll_moves)


if __name__ == "__main__":
    cube = shuffle_cube(create_cube(), n_moves=15, seed=67)
    print_cube(cube)
    alg = CFOP_solve(cube)
    print(alg)
    print_cube(parse_algorithm(alg, cube))
