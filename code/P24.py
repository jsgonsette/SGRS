# MIT License

# Copyright (c) [2020] [Jean-Sébastien Gonsette]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__author__ = "Jean-Sébastien Gonsette"
__year__ = 2019

import numpy as np

# Encoding of every pieces, +1 is a notch, -1 a hole and 0 is for flat
# We have 4 sets for left, up, right and down sides. 
# The additional number give the allowed rotations 0: none, 1: 180°, 2: 90°
pieces = {
    'A': [(1,-1,-1), (-1,1,1), (0,1,-1), (0,1,1), 0],
    'B': [(1,1,-1), (1,0,0), (1,1,0), (1,0,-1), 0],
    'C': [(1,1,-1), (-1,1,0), (1,1,0), (0,0,-1), 0],
    'D': [(-1,1,-1), (0,0,1), (-1,1,1), (1,-1,0), 0],
    'E': [(0,0,0), (0,-1,0), (1,1,-1), (1,-1,1), 0],
    'F': [(1,-1,-1), (1,-1,1), (0,1,0), (0,-1,1), 0],
    'G': [(1,-1,1), (-1,0,0), (0,-1,1), (0,-1,0), 0],
    'H': [(0,-1,-1), (-1,-1,1), (0,1,0), (0,-1,1), 1],
    'I': [(0,1,-1), (-1,-1,0), (-1,0,0), (0,1,0), 1],
    'J': [(-1,1,0), (0,1,0), (-1,-1,1), (0,0,0), 0],
    'K': [(0,0,0), (1,1,0), (1,-1,1), (1,1,-1), 0],
    'L': [(1,-1,-1), (0,-1,0), (1,-1,0), (1,-1,1), 0],
    'M': [(0,-1,1), (1,-1,1), (0,0,0), (0,0,0), 0],
    'N': [(1,-1,1), (0,0,-1), (0,-1,0), (-1,1,0), 1],
    'O': [(0,0,0), (1,1,-1), (-1,-1,1), (0,0,0), 2],
    'P': [(-1,-1,1), (0,0,1), (0,-1,1), (1,-1,0), 0],
    'Q': [(-1,1,-1), (0,1,-1), (-1,1,1), (-1,1,-1), 0],
    'R': [(0,0,0), (0,0,0,), (-1,1,-1), (-1,0,1), 0],
    'S': [(-1,1,0), (0,1,-1), (0,0,0,), (-1,0,0), 1],
    'T': [(-1,-1,1), (0,1,-1), (0,-1,1), (-1,1,-1), 0],
    'U': [(1,0,-1), (0,-1,0), (-1,1,1), (-1,0,0), 0],
    'V': [(-1,-1,1), (0,0,0), (0,1,0), (1,1,-1), 0],
    'W': [(-1,1,1), (0,-1,-1), (1,0,-1), (0,0,0), 0],
    'X': [(0,1,0), (-1,1,0), (0,-1,-1), (0,0,0), 2],
    'Y': [(1,0,0), (0,-1,0), (0,0,0), (-1,0,0), 0],
    'Z': [(0,-1,0), (-1,1,1), (-1,0,0), (-1,1,-1), 1],
    '0': [(1,-1,-1), (-1,1,1), (0,0,0), (1,0,-1), 1],
    '1': [(0,0,1), (0,1,0), (-1,0,1), (-1,-1,1), 0],
    '2': [(1,0,-1), (0,0,1), (0,0,0), (1,-1,0), 0],
    '3': [(1,1,-1), (0,0,0), (-1,1,-1), (0,-1,0), 0],
    '4': [(0,0,0), (0,-1,0), (0,-1,1), (0,0,0), 0],
    '5': [(1,-1,-1), (-1,1,-1), (0,0,0), (-1,1,0), 0],
    '6': [(-1,1,0), (1,-1,-1), (0,0,0), (0,1,0), 1],
    '7': [(0,0,1), (-1,1,0), (0,0,0), (-1,-1,1), 0],
    '8': [(1,-1,1), (1,-1,0), (0,-1,1), (0,0,0), 1],
    '9': [(1,0,0), (0,1,0), (1,0,-1), (0,0,0), 1],
}

# Grid size, can be changed to solve smaller grids
SIZE = 5

# Keep track of pieces in use during processing
usage = [False] * len (pieces)


def neg_interface (interface):
    """Negate the side of a puzzle
    
    interface       a set (x, y, z) giving what the side looks like
    """
    b= *(-p for p in reversed (interface)),
    return b


def char_to_index (char):
    """Convert a piece name (A-Z + 0-9) to an index"""

    index = ord (char) - ord ('A')
    if index < 0: index =  ord (char) - ord ('0') + 26
    return index

def index_to_char (index):
    """Convert an index to a piece name (A-Z + 0-9)"""

    if index < 0: return '*'
    elif index < 26: return chr (ord ('A') + index)
    else: return chr (ord ('0') + index - 26)


def iter_pieces (i_left, i_down, rotation='natural'):
    """Iterate on all the pieces that fit on its left and down side

    i_left:     Left side of the piece we look for (None if not used)
    i_down:     Down side of the piece we look for (None if not used)
    rotation:   'none' Do not try rotate pieces
                'all' try all 4 rotations
                'natural' try the natural rotations for each piece (as encoded)"""

    for key in pieces:

        left, up, right, down, symmetry = pieces [key]
        if rotation == 'all': symmetry = 2
        elif rotation == 'none': symmetry = 0
        
        fit = False
        for rot in range (4):
            if symmetry == 0 and rot > 0: continue
            if symmetry == 1 and rot not in (0, 2): continue

            fit_rotation = True
            if rot == 0:
                if i_left is not None and left != i_left: fit_rotation = False      
                if i_down is not None and down != i_down: fit_rotation = False
            elif rot == 1:
                if i_left is not None and up != i_left: fit_rotation = False      
                if i_down is not None and left != i_down: fit_rotation = False
            elif rot == 2:
                if i_left is not None and right != i_left: fit_rotation = False      
                if i_down is not None and up != i_down: fit_rotation = False
            else:
                if i_left is not None and down != i_left: fit_rotation = False      
                if i_down is not None and right != i_down: fit_rotation = False
            
            if fit_rotation:
                fit = True
                break

        if not fit: continue

        index = char_to_index (key)
        if usage [index] == True: continue
        
        usage [index] = True
        yield key, rot
        usage [index] = False


def print_grid (grid_content):
    """Print grid content (without rotation)"""
    
    print ("")
    for y in range (SIZE-1, -1, -1):
        line = ' '.join ([index_to_char (grid_content [x, y]) for x in range (SIZE)])
        print (line)


# Grid content (letter), corresponding rotation, and generator used during processing
grid_content = -np.ones ([SIZE,SIZE], dtype=int)
grid_rot = np.zeros ([SIZE,SIZE], dtype=int)
generators = [None] * SIZE*SIZE

# Iterate
x = y = 0
count = 0

# Processing until we fail or succeed
while x < SIZE and y < SIZE and x >= 0 and y >= 0:
    
    count += 1
    if count % 1000 == 0: print_grid (grid_content)

    # Create a generator at this position if needed
    generator = generators [y*SIZE+x]
    if not generator:
        left_piece = pieces [index_to_char (grid_content [x-1, y])] if x > 0 else None
        down_piece = pieces [index_to_char (grid_content [x, y-1])] if y > 0 else None
        
        i_left = i_down = None
        if left_piece: 
            rot = grid_rot [x-1, y]
            i_left = neg_interface (left_piece [(2 + rot) % 4])
        if down_piece: 
            rot = grid_rot [x, y-1]
            i_down = neg_interface (down_piece [(1 + rot) % 4])
        
        generator = iter_pieces (i_left, i_down, rotation='natural')
        generators [y*SIZE+x] = generator

    # Get next possibility
    try:
        key, rot = next (generator)
        grid_content [x, y] = char_to_index (key)
        grid_rot [x, y] = rot

        # Move on if successful
        x += 1
        if x >= SIZE:
            y +=1
            x = 0

    # Move back if no solution
    except:
        grid_content [x, y] = -1
        grid_rot [x, y] = 0
        generators [y*SIZE+x] = None
        
        x -= 1
        if x < 0:
            y -= 1
            x = SIZE-1            

print_grid (grid_content)
print ("Finish")
