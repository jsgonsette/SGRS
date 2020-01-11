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


from Tools.vocabulary import Vocabulary
from Tools.mendeliev import build_mendeleiev_list
import numpy as np
import re


# Exemple grid
# The 8 directions are encoded with values 0-7
grid_0 = ['UNL', 'XEM', 'EEP']
grid_0_d = ['065', '746', '212']

# Question a. 
grid_A = [
    'USADUS', 'IBPREE', 'ESEJAR',
    'TAUNEO', 'UCGATD', 'NEHIHA']
grid_dir_A = ['676064', '160214', '604156', '025345', '272432', '004132']

# Question b
grid_B = [
    'OILRAUIM', 'TIEDLORT', 'NTSAMOTE',
    'TLBBAIOR', 'RESIGRPI', 'ESOIDDNP',
    'NMERESEP', 'PSNUSEON']
grid_dir_B = [
    '06774466', '67605444', '60462476',
    '67344345', '00041662', '60203544',
    '11410175', '21422444']

# Question c
grid_C = [
    'AEADVCAAE', 'NA-LEELSV', 'MEVZBAINU',
    'UOAELSEDU', 'C-CUISEST', 'EONVICMAE',
    'RGVOIRATE', 'EALOPECJT', 'SASNISVEN']

grid_dir_C = [
    '677765646', '776650665', '116665144',
    '705205635', '727414424', '706032244',
    '607310433', '025641334', '101402302']


def iter_next_letter (position, grid, grid_dir, usage):
    """Iterate on next possible letters from a given position
    
    position:       (x, y) start position
    grid:           Target grid
    grid_dir        Target grid (directions)
    usage:          Common array to lock used letters
    """

    steps = [(1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1), (1,1)]

    width = len (grid)
    x, y = position
    step_str = grid_dir [position [1]][position [0]]
    step = steps [ord (step_str) - ord ('0')]

    while True:
        x += step [0]
        y += step [1]
        if x >= width or y >= width or x < 0 or y < 0: break
        if usage [y, x]: continue
        
        usage [y, x] = 1
        yield (x, y), grid [y][x]
        usage [y, x] = 0


def find_words_at (voc, grid, grid_dir, start, length_min=2):
    """Find all possible words starting at a given position"""

    MAX_LEN = 16
    width = len (grid)

    # Housekeeping material
    generators = [None] * width * width
    prev_pos = [(0,0)] * width * width
    usage = np.zeros ([len (grid), len (grid)])
    propositions = {(x, y): set () for x in range (width) for y in range (width)}
  
    # start position
    level = 1
    position = start
    prev_pos [0] = start
    usage [start [1], start [0]] = 1
    message = grid [start [1]][start [0]]

    while level > 0:

        if generators [level] is None:        
            generators [level] = iter_next_letter (position, grid, grid_dir, usage)

        try:
            # Save current position and try to go forward
            position, letter = next (generators [level])         
            prev_pos [level] = position

            # Check we have either a valid word, or the begining of a valid word
            tentative_raw = message + letter
            tentative = tentative_raw.replace ('-', '')

            # - Valid word: register it and continue deeper
            if voc.is_valid_word (tentative) and len (tentative_raw) >= length_min:
                # Add them to all the grid position they go through
                for j in range (len (tentative_raw)):
                    propositions [prev_pos [j]].add (tentative_raw)
                move = 1

            # - Not a valid word, but valid start: continue deeper
            elif voc.is_valid_word_start (tentative):
                move = 1

            # - Continue to test this level
            else:
                move = 0

        # Iterator exhausted at this level, go backward
        except:
            move = -1

        if move == 1:
            message += letter            
            level += 1

        elif move == -1:
            generators [level] = None
            message = message [:-1]
            level -= 1
            position = prev_pos [level]
        
    return propositions


def make_proposals (voc, grid, grid_dir):
    """Make propositions to solve the puzzle"""

    width = len (grid)
    proposal_list = {(x, y): set() for x in range (width) for y in range (width)}

    # For each position, find the longest words that can start there
    for x in range (width):
        for y in range (width):
            words = find_words_at (voc, grid, grid_dir, (x,y))

            for pos in words:
                for w in words [pos]:
                    proposal_list [pos].add (w)


    for x in range (width):
        for y in range (width):
            print ("\n\nWords crossing case {}, {} ({})".format (x, y, grid [y][x]))
            print (proposal_list [(x, y)])



def check_mendeliev ():
    """Call this function to check if any Mendeleiv element fit any grid"""
    voc = Vocabulary ('./code/Tools/libWizium.dll', None)

    mendel_list, dico_reverse = build_mendeleiev_list ()
    voc.wiz.dic_add_entries (mendel_list)

    make_proposals (voc, grid_A, grid_dir_A)
    make_proposals (voc, grid_B, grid_dir_B)
    make_proposals (voc, grid_C, grid_dir_C)

    print (dico_reverse ['TPEJVN'])
    print (dico_reverse ['RISR'])



# Load dictionary
WIZ_PATH = './code/Tools/libWizium.dll'
DICO_PATH = './code/Fr_Simple.txt'
voc = Vocabulary (WIZ_PATH, DICO_PATH)

# Generate propositions
if True:
    make_proposals (voc, grid_A, grid_dir_A)

if False:
    make_proposals (voc, grid_B, grid_dir_B)

if False:
    make_proposals (voc, grid_C, grid_dir_C)



# Call this function to check for Mendeleiv words
if False:
    print ("\nChecking for Mendeleiev elements")
    check_mendeliev ()
