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


import itertools
import re
import numpy as np
from Tools.mendeliev import build_mendeleiev_list


length_patterns = [
    [2,3,3,3,4,5,6],
    [5,7,7,7],
    [1,1,5,6,6,7],
    [5,6,15],
    [5,7,7,7],
    [1,2,2,3,3,3,5,7],
    [1,1,1,2,2,4,4,11],
    [1,4,21],
    [1,1,1,3,5,15],
    [1,1,1,3,4,4,5,7],
    [1,1,4,5,5,10],
    [1,2,4,4,15],
    [1,1,1,1,2,3,3,4,5,5],
    [1,2,2,4,17],
    [2,2,3,3,3,4,4,5],
]

voyels_patterns = [
    [(0,0), (1,2), (3,2), (4,3), (6,5)],
    [(0,0), (0,4), (1,3), (2,2), (3,1)],
    [(2,0), (2,4), (3,2), (4,0), (5,3)],
    [(0,0), (0,4), (1,0), (2,3), (2,9)],
    [(0,0), (0,4), (1,3), (2,2), (3,1)],
    [(1,1), (2,1), (3,0), (4,2), (7,3)],
    [(2,0), (3,0), (4,1), (5,3), (7,5)],
    [(0,0), (1,0), (2,3), (2,9), (2,15)],
    [(2,0), (5,0), (5,4), (5,8), (5,14)],
    [(0,0), (4,3), (5,3), (6,1), (7,1)],
    [(3,0), (3,4), (4,4), (5,3), (5,9)],
    [(1,1), (4,0), (4,4), (4,8), (4,14)],
    [(0,0), (3,0), (4,1), (5,0), (7,3)],
    [(0,0), (2,1), (4,3), (4,9), (4,15)],
    [(0,1), (1,0), (2,0), (3,0), (5,1)],
]


def make_rows (string):

    rows = []    
    cut_points = sorted (list (set (string)))
    trunk = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    pos = 0
    for cut in cut_points:
        while trunk [pos] != cut:
            pos += 1
        rows.append (trunk [0:pos+1])
        trunk = trunk [pos+1::]
        pos = 0

    if len (trunk): rows.append (trunk)
    return rows


def make_towers (rows):

    # Get all rows and group them by length
    items = [(row, len (row)) for row in rows]
    groups = itertools.groupby (items, key=lambda x: x [1])

    # Look at each group and take all the permutations of rows that have the same length
    perms_list = []
    for length, items in groups :
        slices = [item [0] for item in list (items)]
        perms = list (itertools.permutations (slices))
        perms_list.append ((perms, length))

    # Keep our list of permutations sorted by length
    perms_list = sorted (perms_list, key=lambda x: x [1])

    # Now take the product of each set of permutations to generate all the possible arrangements
    towers_pieces = [list (p [0]) for p in perms_list]
    towers = list (itertools.product (*towers_pieces))

    # Make our towers flat (to have simple list of strings)
    flat_towers = []
    for tower in towers:
        flat_tower = []
        for pieces in tower:
            flat_tower.extend (pieces)
        
        flat_towers.append (flat_tower)

    return flat_towers


def get_words (path):
    
    with open (path, 'r') as f:
        words = f.readlines ()
    
    words = [re.sub('[^a-zA-Z]+', '', s) for s in words]
    return words


def get_pattern_index (string):

    # Slice the word
    rows = make_rows (string.upper ())
    lengths = sorted ([len (row) for row in rows])

    # Compare with length with patterns we look for
    match = [lengths == pattern for pattern in length_patterns]
    if not any (match): return -1

    for i in range (len (match)):
        if match [i]: return i


def check_voyels_patterns (string, pattern):
    rows = sorted (make_rows (string.upper ()), key=lambda x: len (x))
    towers = make_towers (rows)

    for tower in towers:

        found = True
        for position in pattern:
            if tower [position [0]][position [1]] not in ('A', 'E', 'I', 'O', 'U'):
                found = False
                break

        if found: break

    return found


def num_towers (num_cubes, max_row=0, oracle=None):

    if max_row == 0: max_row = num_cubes
    if max_row == 1: return 1

    # Oracle stores how many towers exists, given a total amount of cubes (x) and a maximal row length (y)
    if oracle is None: 
        oracle = np.zeros ([num_cubes+1, num_cubes+1], dtype=int)
        oracle [:, 1] = 1

    # How many time can we use a row with this maximum length ?
    n = num_cubes // max_row

    # Compute recursively
    num_combi = 0
    for i in range (0,n+1):
        
        # Try with oracle
        x = num_cubes - i*max_row
        y = max_row -1
        num = oracle [x, y]
        
        # If this answer is not knwon yet, go deeper
        if num == 0:
            num = num_towers (x, y, oracle)

        num_combi += num

    # Store answer in oracle
    oracle [num_cubes, max_row] = num_combi
    return num_combi



def check_towers (words):
    match_words = []
    for i in range (len (length_patterns)): match_words.append ([])

    for w in words :
        pattern_idx = get_pattern_index (w)
        if pattern_idx >= 0:

            result = check_voyels_patterns (w, voyels_patterns [pattern_idx])
            if result: 
                match_words [pattern_idx].append (w)

    print ("List of possible words at each tower position:")
    for matches in match_words:
        print (matches)


def check_mendeleiev ():

    words, dico_reverse = build_mendeleiev_list ()
    check_towers (words)
    exit ()


def print_tower (word):

    towers = make_towers (make_rows (word))
    print ('\n' + word + ':')
    for row in towers [0]:
        print (row)


# Add dictionary, and numbers to solve last tower
words = get_words ('./code/FR_Simple.txt')
words.extend (["SEIZE", "QUINZE", "DIXSEPT", "DIXHUIT", "DIXNEUF", 
    "VINGT", "VINGTETUN", "VINGTDEUX", "VINGTROIS", "VINGTQUATRE", "VINGTCINQ", "VINGTSIX", "VINGTSEPT", "VINGTHUIT", "VINGTNEUF"
    "TRENTE", "TRENTEETUN", "TRENTEDEUX", "TRENTETROIS", "TRENTEQUATRE", "TRENTECINQ", "TRENTESIX", "TRENTESEPT", "TRENTEHUIT", "TRENTENEUF"])

print ("Found {} words in dictionary".format (len (words)))

check_towers (words)

print ("\nNumber of different towers with 25 blocs: " + str (num_towers (25)))
print ("Which corresponds to the discovery year of Nobelium (No)")


print ("\nChecking for Mendeleiev elements")
check_mendeleiev ()
