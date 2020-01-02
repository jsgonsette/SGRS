import numpy as np
from Tools.vocabulary import Vocabulary
from Tools.countries import countries, cities
import re

def develop_middle (string, direction='up'):
    """Develop each row of the diamond from a starting row"""

    up = string.upper ()
    ups = []

    while len (up) > 1:
        out = ''
        for idx, s in enumerate (up [:-1]):
            sn = up [idx +1]

            if direction == 'up':
                out += chr ((ord (s)-ord('A') + ord (sn)-ord('A'))%26 + ord('A'))
            elif direction == 'down':
                out += chr ( (ord(s)-ord('A') - ord(sn)+ord('A')) % 26 + ord('A') )

        up = out
        ups.append (up)

    return ups


def next_char (s):
    """Next alphabet character, modulo 26"""
    return chr (ord('A') + ((ord (s)-ord('A') +1) % 26))


def get_diamond_coeffs (length, direction='up'):
    """Return weigths of each letter at the middle of a diamond shape,
    regarding their contribution to the top letter"""
    
    coeffs = np.ones ([length], dtype=int)
    half = length //2 
    odd = length % 2

    # Do the first half
    for idx in range (half+odd):
        for i in range (1, length -idx-1):
            coeffs [i] += coeffs [i-1]

    # Mirror the second part
    for idx in range (half):
        coeffs [idx] = coeffs [length-1-idx]
    
    # For down direction, we have to negate one coeff out of 2
    if direction == 'down':
        parity = [1, -1] * (half +1)
        coeffs = [c * p for c, p in zip (coeffs, parity)]

    return coeffs


def predic_top (string, coeffs=None):
    """Predict top letter of diamond from starting row, without explicitly developing each intermediate row
    """

    # For computation coefficients of each base letter
    if coeffs is None: coeffs = get_diamond_coeffs (len (string))
    top = 0

    # Process base letters, 2 by 2, starting from extremities
    for s, c in zip (string, coeffs):
        top += (ord (s)-ord ('A')) * c

    return chr (ord('A') + top%26)


def predic_down (string, coeffs=None):
    """Predict down letter of diamond from starting row, without explicitly developing each intermediate row
    """

    if coeffs is None: 
        coeffs = get_diamond_coeffs (len (string), direction='down')
    return predic_top (string, coeffs)


# def find_base (voc, base_pattern, final_letter, direction='up', prefix=''):

#     coeffs = get_diamond_coeffs (len (base_pattern), direction)

#     var = [idx for idx, s in enumerate (base_pattern) if s == '*']
#     fill = ['A'] * len (var)
#     pos = 0

#     soluces = []
#     scores = []

#     while True:

#         # Make word to test by replacing '*' with letters        
#         w = list (base_pattern)
#         for idx, f in zip (var, fill):
#             w [idx] = f
#         word = ''.join (w)

#         # Make the word evolve and check the top letter
#         # top = develop_middle (word, direction='up')
#         top = predic_top (word, coeffs=coeffs)
#         if top [-1] == final_letter: 
#             score = voc.is_valid_start (prefix + word, can_extend=True)
#             if score > 0:
#                 soluces.append (prefix + word)
#                 scores.append (score)
            
#         # Move on the pattern to replace '*'
#         while pos < len (fill):
#             fill [pos] = next_char (fill [pos])
#             if fill [pos] == 'A': 
#                 pos += 1
#                 continue
#             break
#         if pos >= len (fill): break
#         pos = 0

#     return soluces, scores 
    

# def find_base_list (voc, pattern_list, final_letter, direction='up', prefix_list=None):
    
#     soluces = []
#     scores =  []
#     if not prefix_list: prefix_list = [''] * len (pattern_list)

#     for prefix, p in zip (prefix_list, pattern_list):
#         soluce_list, score_list = find_base (voc, p, final_letter, direction=direction, prefix=prefix)
#         soluces.extend (soluce_list)
#         scores.extend (score_list)

#     return soluces, scores

def print_diamond (lines, direction='up'):
    width = len (lines [0])

    if direction=='up':
        for idx, line in enumerate (reversed (lines)):
            print (' ' * (width-idx) + ' '.join (line) )
    else:
        for idx, line in enumerate (lines):
            print (' ' * idx + ' '.join (line) )

print ("Some checks on the exemple\n----------------")
print (predic_top ("EXEMPLE"))
print (predic_top ("EXEMPL"))
print (predic_top ("XEMPLE"))

print (predic_down ("EXEMPLE"))
print (predic_down ("EX"))
print (predic_down ("XE"))
print (predic_down ("EXE"))

print (predic_down ("EXEMPL"))
print (predic_down ("XEMPLE"))
print (predic_down ("XEMPL"))

print ("\nPrint coefficients to solve the system of equations\n----------------")

up = [3,4,5,6,10,11,13,18]
down = [2,6,7,10,12,19]
for u in up:
    print ('up ' + str (u) + str (get_diamond_coeffs (u, direction='up')))

for d in down:
    print ('down ' + str (d) + str (get_diamond_coeffs (d, direction='down')))


print ("\nSolution\n----------------")

print_diamond (develop_middle ("MONSLALOUVIERENAMUR", direction='up'), direction='up')
print_diamond (develop_middle ("MONSLALOUVIERENAMUR", direction='down'), direction='down')

exit ()
