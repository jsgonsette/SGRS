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


def letter36_to_idx (letter):

    o = ord (letter)
    if o >= ord ('A') and o <= ord ('Z'): return o - ord ('A')
    elif o >= ord ('0') and o <= ord ('9'): return o - ord ('0') + 26
    return -1


def adfgvx (string, key, square, reverse=False, use_null=True):
    
    heads = 'ADFGVX'
    string = string.upper ()
    key = key.upper ()
    square = square.upper ()

    # Encryption/decryption grid
    dico_encrypt = {}
    dico_decrypt = {}
    for x in range (6):
        for y in range (6):
            dico_encrypt [square [y*6+x]] = heads [y] + heads [x]
            dico_decrypt [heads [y] + heads [x]] = square [y*6+x]

    # Permutation key
    key_ex = [(ord (s), idx) for idx, s in enumerate (key)]
    key_ex = sorted (key_ex, key=lambda x: x [0])
    key_perm = [k [1] for k in key_ex]

    key_perm_inv = [0] * len (key_perm)
    for idx, k in enumerate (key_perm):
        key_perm_inv [k] = idx

    if reverse == False:

        # First encryption step
        encrypted = ''.join ([dico_encrypt [s] for s in string])
        encrypted_2 = ''
        
        # Second encryption step -> permutation

        # - number of rows required to write the message
        num_rows = len (encrypted) // len (key)
        if num_rows * len (key) < len (encrypted): num_rows +=1

        # - Read the encrypted message column by column, with column transposition
        for idx in range (num_rows * len (key)):
            row = idx % num_rows
            column = key_perm [idx // num_rows]

            target_idx = row * len (key) + column
            if (target_idx < len (encrypted)): 
                encrypted_2 += encrypted [target_idx]
            else:
                encrypted_2 += '0'

        if use_null: return encrypted_2.replace ('0', 'A')        
        else: return encrypted_2.replace ('0', '')

    else:

        # Undo permutation
        # - Number of rows
        num_rows = len (string) // len (key)
        if num_rows * len (key) < len (string):
            
            if use_null == True: return None
            
            num_rows +=1
            nulls = num_rows * len(key) - len (string)

            insertion = sorted (key_perm_inv [-nulls::])
            insertion = [(i+1)*(num_rows)-1 for i in insertion]
            for i in insertion:
                string = string [0:i] + '0' + string [i::]

        encrypted_1 = ''

        for idx in range (len (string)):

            column = key_perm_inv [idx % len (key)]
            row = idx // len (key)

            target_idx = num_rows * column + row
            if (target_idx < len (string)): 
                encrypted_1 += string [target_idx]
            else:
                encrypted_1 += 'A'

        # Decrypt with grid
        plain = ''
        for idx in range (len (encrypted_1) // 2):
            bi = encrypted_1 [idx*2:idx*2+2]
            if bi != '00':
                plain += dico_decrypt [bi]

        return plain



