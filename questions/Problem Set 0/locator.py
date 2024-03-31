from typing import Any, Set, Tuple
from grid import Grid
import utils

def locate(grid: Grid, item: Any) -> Set[Tuple[int,int]]:
    '''
    This function takes a 2D grid and an item
    It should return a list of (x, y) coordinates that specify the locations that contain the given item
    To know how to use the Grid class, see the file "grid.py"  
    '''
    myset = set() #empty set
    count = 0
    height = grid.height
    width = grid.width
    for c in range(width) :
        for r in range(height):
           if grid[c,r] == item:
                t : tuple = (c,r)
                myset.add(t)
    return myset


# grid = Grid.GridFromArray([['a','b','c','d'],['b','c','a','d'],['d','c','b','a']])
# search = 'a'
# print(locate(grid,search))

# # ['a','b','c','d'],
# # ['b','c','a','d'],
# # ['d','c','b','a']
# # print(grid.width)
# # print(grid.height)