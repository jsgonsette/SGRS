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


import Tools.ciphers as ciphers
from Tools.vocabulary import Vocabulary
from Tools.mendeliev import mendeleiv_fr
import re
import io
import itertools as it


grid =[
    'HDIIGRBQGEGQGBIH-',
    'VIUVBSSY-CQSCBCVB',
    'UIKI-EOEB   -  JR',
    'IGFIRBG-S      VC',
    'UI-EBDIXR      -K',
    'UMKEPQGESADJ-HMRI',
    'DIITDMFGAJJSBKRMR',
    'GPGGEDA-PESFUAM-U',
    'R-BH-TUSAGDEKAVTI',
    'IDTDQEEFMA-GIDAAI'
]


# grid =[
#     'HDIIGRBQGEGQGBIH-',
#     'VIUVBSSY-CQSCBCVB',
#     'UIKI-EOEBAUT-OUJR',
#     'IGFIRBG-SRDESPAVC',
#     'UI-EBDIXRLOMBES-K',
#     'UMKEPQGESADJ-HMRI',
#     'DIITDMFGAJJSBKRMR',
#     'GPGGEDA-PESFUAM-U',
#     'R-BH-TUSAGDEKAVTI',
#     'IDTDQEEFMA-GIDAAI'
# ]

def grid_rot (grid, shift):
    new_grid = [ciphers.rotate (line, shift) for line in grid]
    return new_grid

def grid_print (grid):
    """Print the grid content"""
    for line in grid:
        print (' '.join (line))

def grid_transpose (grid):
    """Return a transposed copy of the grid"""
    new_grid = []
    for idx in range (len (grid [0])):
        line = ''.join (row [idx] for row in grid)
        new_grid.append (line)

    return new_grid

def grid_extract (grid, x, y, w, h):
    """Extract a part of the grid, at a given location
    and for some widht and height"""

    new_grid = []
    for cy, line in enumerate (grid):
        if cy < y or cy >= y+h: continue
        new_line = ''

        for cx, s in enumerate (line):
            if cx < x or cx >= x+w: continue
            new_line += s

        new_grid.append (new_line)

    return new_grid


def read_rectangle (extract):
    """Given some rectangle of letters, read it in different ways"""
    texts = []

    rectangles = [extract, grid_transpose (extract)]

    for rectangle in rectangles:
        texts.append (''.join (rectangle))
        texts.append (''.join (reversed (rectangle)))
        flip = [''.join (reversed (w)) for w in rectangle]
        texts.append (''.join (flip))
        texts.append (''.join (reversed (flip)))

    return texts


def grid_get_extracts_around (grid, x, y):
    """Extract all the different ways to read grid content from a sub rectangle
    around a given position"""

    assert (grid [y][x] == '-')

    width= len (grid [0])
    height= len (grid)

    extracts = []

    # Try all rectangles fitting in the grid, and including the box (x, y)
    for cx in range (0, x+1):
        for w in range (x-cx+1, width-cx+1):
            for cy in range (0, y+1):
                for h in range (y-cy+1, height-cy+1):

                    # Extract this part of the grid and check we are not bumping in another rectangle
                    extract = grid_extract (grid, cx, cy, w, h)
                    flat = ''.join (extract)
                    if flat.count ('-') > 1: continue
                    if flat.count (' ') > 0: continue
                    
                    # Now read the content of this extract in different ways
                    extracts.extend (read_rectangle (extract))

    return extracts


def get_words (path):
    """Make a list of words from a .txt file"""
    
    with io.open (path, mode='r', encoding='utf-8') as f:
        words = f.readlines ()
    
    # words = [w [0:w.find (' ')] if w.count (' ') >= 1 else w for w in words]
    words = [re.sub('[éêèëÉÈÊË]+', 'E', s) for s in words]
    words = [re.sub('[ùûÛüÜÙ]+', 'U', s) for s in words]
    words = [re.sub('[ïîÏÎ]+', 'I', s) for s in words]
    words = [re.sub('[äâÄÂàÀ]+', 'A', s) for s in words]
    words = [re.sub('[ôöÔÖ]+', 'O', s) for s in words]
    words = [re.sub('[ç]+', 'C', s) for s in words]
    words = [re.sub('[^a-zA-Z]+', '', s) for s in words]
    words = [w.upper () for w in words]
    return words



# Make a dictionary with the animal names
WIZ_PATH = './code/Tools/libWizium.dll'
DICO_PATH = './code/Animaux.txt'
voc = Vocabulary (WIZ_PATH, DICO_PATH)

# Simple loading of animal anmes
animals = get_words (DICO_PATH)

# Coordinates of the numbers in the grid
coordinates = [(1,8), (2,4), (4,2), (4,8), (7,3), (7,7), (8,1), (10,9), (12,5), (15,4), (15,7), (16,0)]

# Candidates keys
keys = list (mendeleiv_fr)
keys.extend (animals)
keys.extend ('BCDEFGHIJKLMNOPQRSTUVWXYZ')
keys.extend (['LI', 'BE', 'NE', 'NA', 'MG', 'AL', 'SI', 'CL', 'AR', 'CA', 
    'SC', 'TI', 'CR', 'MN', 'FE', 'CO', 'NI', 'CU', 'ZN', 'GA', 'GE', 'AS', 
    'SE', 'BR', 'KR', 'RB', 'SR', 'ZR', 'NB', 'MO', 'TC', 'RU', 'RH', 'PD', 
    'AG', 'CD', 'IN', 'SN', 'SB', 'TE', 'XE'])
keys = [k.upper () for k in keys]

# Test all coordinates
count = 0
for x, y in coordinates:

    # Extract all possible rectangles
    print ('\nTest around {}, {}'.format (x, y))
    extracts = grid_get_extracts_around (grid, x, y)
    extracts = sorted (extracts, key=lambda x: len (x))

    # Test each rectangle with each key
    for extract in extracts:
        if len (extract) < 6: continue
        count += 1

        for key in keys:

            key = key.upper ()
            plain_0 = ciphers.vigenere (extract, key, reverse=True).replace ('-', '')
            plain_1 = ciphers.vigenere (extract, key, reverse=False).replace ('-', '')
            plain_2 = ciphers.vigenere (extract.replace ('-', ''), key, reverse=True)
            plain_3 = ciphers.vigenere (extract.replace ('-', ''), key, reverse=False)
    
            for plain in (plain_0, plain_1, plain_2, plain_3):
                if voc.is_valid_word (plain): print ('{} from {} with key {}'.format (plain, extract, key))


print ("{} rectangles tested".format (count))


