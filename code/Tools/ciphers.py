import numpy as np
from itertools import permutations


def rotate (string, shift):
    output = ""
    for s in string.upper ():
        o = ord (s) + shift
        if o < ord ('A'): o += 26
        if o > ord ('Z'): o -= 26
        output += chr (o)
    return output


def vigenere (string, key, reverse=False):
    n = len (key)
    output = ""

    for idx, s in enumerate (string.upper ()):
        shift = ord (key [idx%n]) - ord ('A') 
        if reverse: shift = -shift

        o = ord (s) + shift
        if o < ord ('A'): o += 26
        if o > ord ('Z'): o -= 26

        output += chr (o)
    return output


def beaufort (string, key):
    n = len (key)
    output = ""

    for idx, s in enumerate (string.upper ()):

        o = ord (key [idx%n]) - (ord (s) - ord ('A'))
        if o < ord ('A'): o += 26
        if o > ord ('Z'): o -= 26

        output += chr (o)
    return output


def play_fair (string, key, reverse=False):

    key = key.upper ()
    string = string.upper ()

    # Key in grid
    skip = 0
    grid = np.zeros ([5,5], dtype=int)
    key_set = set ()
    for idx, s in enumerate (key):
        row = (idx-skip) // 5
        col = (idx-skip) % 5
        if s == 'J': s = 'I'

        if s not in key_set:
            key_set.add (s)
            grid [row, col] = ord (s)
        else:
            skip += 1

    # Complete grid
    idx -= skip
    fill = 'A'
    for idx in range (idx+1,25):
        
        while fill in key_set:
            fill = chr (ord (fill) + 1)
            if fill == 'J': 
                fill = 'K'
                continue
        
        key_set.add (fill)
        row = idx // 5
        col = idx % 5        
        grid [row, col] = ord (fill)

    output = ''
    for idx in range (len (string) // 2):
        l1 = string [idx*2]
        l2 = string [idx*2 +1]
        if l1 =='J': l1 = 'I'
        if l2 =='J': l2 = 'I'
        # if l1 == l2: l2 = 'X'

        p1 = np.squeeze (np.where (grid == ord (l1)))
        p2 = np.squeeze (np.where (grid == ord (l2)))

        move = 1 if not reverse else -1
        if p1 [0] == p2 [0] and p1 [1] == p2 [1]:
            l1 = grid [(p1 [0]+move) % 5, (p1 [1]+move) % 5]
            l2 = grid [(p2 [0]+move) % 5, (p2 [1]+move) % 5]
        elif p1 [0] == p2 [0]:
            l1 = grid [p1 [0], (p1 [1]+move) % 5]
            l2 = grid [p2 [0], (p2 [1]+move) % 5]
        elif p1 [1] == p2 [1]:
            l1 = grid [(p1 [0]+move) % 5, p1 [1]]
            l2 = grid [(p2 [0]+move) % 5, p2 [1]]
        else:
            l1 = grid [p1 [0], p2 [1]]
            l2 = grid [p2 [0], p1 [1]]

        output += chr (l1) + chr (l2)
     
    return output


