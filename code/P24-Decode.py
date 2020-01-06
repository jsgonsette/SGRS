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


import math
import numpy as np
import itertools as it
import Tools.ciphers as ciphers


# Message to decode
msg = "FGGFADADDGDAGVFVXGGAAGAFAGDGGFVVVVADGGDGGAGAGGAGFDFDADVFAFDAVVVDDXGAVVVVFVFVGFVDDFFAAG"

# Square keys we got by reordering puzzle pieces
# R W J 8 3 O
# E A G Q H 6
# X F D L C Y
# K Z T I 1 2
# V P N B U 5
# 4 S 9 0 7 M

key_square_0 = "rwj83oeagqh6xfdlcykzti12vpnbu54s907m"
key_square_1 = "o6y25M3HC1U78QLIb0jgdtn9wafzpsrexkv4"
key_square_2 = "m709s45ubnpv21itzkycldfx6hqgaeo38jwr"
key_square_3 = "4vkxerspzfaw9ntdgj0bilq87u1ch3m52y6o"

key_square_4 = "o38jwr6hqgaeycldfx21itzk5ubnpvm709s4"
key_square_5 = "rexkv4wafzpsjgdtn98qlib03hc1u7o6y25m"
key_square_6 = "4s907mvpnbu5kzti12xfdlcyeagqh6rwj83o"
key_square_7 = "m52y6o7u1ch30bilq89ntdgjspzfaw4vkxer"

squares = [key_square_0, key_square_1, key_square_2, key_square_3, key_square_4, key_square_5, key_square_6, key_square_7] 

# Letter frequencies in french
freq = {
    'E': 12.10,
    'A': 7.11,
    'I': 6.59,
    'S': 6.51,
    'N': 6.39,
    'R': 6.07,
    'T': 5.92,
    'O': 5.02,
    'L': 4.96,
    'U': 4.49,
    'D': 3.67,
    'C': 3.18,
    'M': 2.62,
    'P': 2.49,
    'G': 1.23,
    'B': 1.14,
    'V': 1.11,
    'H': 1.11,
    'F': 1.11,
    'Q': 0.65,
    'Y': 0.46,
    'X': 0.38,
    'J': 0.34,
    'K': 0.29,
    'W': 0.17,
    'Z': 0.15
    }


def match_column (col_left, col_right, dico_decrypt):
    """Compute a score by matching two columns with each other, based on french 
    letter frequencies. Each pair of letters has some probability of occurence.
    If we get a number instead of a letter, we assume some low frequency"""

    odds = 0.0

    # Take the product of each letter probability
    for left, right in zip (col_left, col_right):
        letter = dico_decrypt [left + right]
        if letter not in freq: letter = 'Z'
        
        odds += math.log (freq [letter] / 100.0)

    # Return mean frequency
    return odds / min (len (col_left), len (col_right))


def find_best_match (key_len, columns, dico_decrypt):
    """Given some columns of letters, compute the score of each 
    possible pairs. Then, return the best way to pair them with each others"""

    # Compute matching scores (each column with all other columns)
    # (If columns have not the same length, just give a bad score)
    scores = np.zeros ((key_len, key_len))
    for idx, column in enumerate (columns):

        odds = []
        for other_idx, other_column in enumerate (columns):
            if other_idx == idx or len (column) != len (other_column): 
                scores [idx, other_idx] = -10.0
                continue

            scores [idx, other_idx] = match_column (column, other_column, dico_decrypt)

    # Find best associations
    indexes = list (range (key_len))
    score = 0.0
    matches = []

    while len (scores):

        # Greedily take best match
        left, right = np.unravel_index(scores.argmax(), scores.shape)          
        matches.append ((indexes [left], indexes [right], scores [left, right]))

        score += scores [left, right]

        # Then remove this pair
        scores = np.delete (scores, [left, right], axis=0)
        scores = np.delete (scores, [left, right], axis=1)

        del indexes [max (left, right)]
        del indexes [min (left, right)]

    # Return mean score of this associations, along with all the pairs
    score /= key_len // 2
    return (score, matches)


def make_columns (string, key_len, col_len, first_indexes):
    """Given some encoded string, the key length and the length of each columns,
    slice the string in different columns. Some columns may have an additional
    caracter, as specified by 'first_indedexes'"""
    
    columns = []
    idx = 0
    for i in range (key_len):
        idx_end = idx + col_len
        if i in first_indexes: idx_end += 1
        column = string [int (round (idx)):int (round (idx_end))]
        idx = idx_end
        columns.append (column)

    return columns


def adfgvx_attack (string, square, key_len):
    """Presume a key length, a known encryption square and a message to decode, 
    then return all the best ways to match columns with each others, along with
    their score"""
    
    heads = 'ADFGVX'
    string = string.upper ()
    square = square.upper ()

    # Encryption/decryption grid
    dico_encrypt = {}
    dico_decrypt = {}
    for x in range (6):
        for y in range (6):
            dico_encrypt [square [y*6+x]] = heads [y] + heads [x]
            dico_decrypt [heads [y] + heads [x]] = square [y*6+x]

    # What are the size of the columns ? Do we have longer columns?
    col_len = len (string) // key_len
    more = len (string) - col_len*key_len
    all_scores = []

    # Try all comibinations for longer columns
    first_col = it.combinations (range (key_len), more)
    for first_indexes in first_col:

        # Create columns from ciphered text
        columns = make_columns (string, key_len, col_len, first_indexes)

        # Find best mathcing
        score, matches = find_best_match (key_len, columns, dico_decrypt)
        all_scores.append ((score, first_indexes, matches))

    return sorted (all_scores, key=lambda x: x [0], reverse=True)


def gen_candidate_keys (first_indexes, matches):
    """Given some pairs of columns matching with each other, 
    given the columns that have an additional caracter (they come first),
    generate all the compatible permutation keys"""

    first_pairs = []
    last_pairs = []
    for (left, right, score) in matches:
        if left in first_indexes: first_pairs.append ((left, right))
        else: last_pairs.append ((left, right))

    for p0 in it.permutations (first_pairs):
        for p1 in it.permutations (last_pairs):
            key = ''.join (chr (left + ord ('A')) + chr (right + ord ('A')) for left, right in p0)
            key += ''.join (chr (left + ord ('A')) + chr (right + ord ('A')) for left, right in p1)

            yield key

"""This program try to decrpty the encoded message, knowing the encryption square,
but without knowledge of the permutation key

This program does not work with odd key length, because it's a bit more complex to program
and I didn't need it. Indeed, my first trial while assuming an even key length was successful.
"""

# Test even length in this range
for length in range (8, 14, 2):
    print ('')
    print ("#" * 30)
    print ('T E S T   L E N G T H   ' + str (length))

    # Test all possible squares
    for key_square in squares:    

        print ("\nTEST SQUARE " + key_square)        
        print ("-" * 30)

        # Make an attack on this square and with this legnth
        all_scores = adfgvx_attack (msg, key_square, length)
        
        # From all the possible pairs of columns, greedily take the most promising
        best = all_scores [0]
        (score, first_indexes, matches) = best

        # Keep it if score is interesting
        if score > -3.6:
            print ("BEST SCORE: " + str (score))
            print ("Longer columns: " + str (first_indexes))
            print ("Column pairing: ")
            for left, right, col_score in matches:
                print ("{}, {} with score {:.02f}".format (left, right, col_score)) 

            # Generate all compatible permutation key, and make the decryption
            for key in gen_candidate_keys (first_indexes, matches):
                print (ciphers.adfgvx (msg, key, square=key_square, reverse=True, use_null=False) + ' (key:{})'.format (key))

        else:
            print ("Not interesting")

