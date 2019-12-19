import itertools
import re


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


words = get_words ('./code/FR_Simple.txt')
print ("Found {} words in dictionary".format (len (words)))

match_words = []
for i in range (len (length_patterns)): match_words.append ([])

for w in words :
    pattern_idx = get_pattern_index (w)
    if pattern_idx >= 0:

        if pattern_idx == 14: print ("[{:02d}]".format (pattern_idx) + " - partial match for " + w )
        result = check_voyels_patterns (w, voyels_patterns [pattern_idx])
        if result: 
            match_words [pattern_idx].append (w)

print ("List of possible words at each tower position:")
for matches in match_words:
    print (matches)

