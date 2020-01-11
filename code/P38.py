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

# Cellular Automaton rule
rule = {
    '000': '0',
    '001': '1',
    '010': '0',
    '011': '1',
    '100': '1',
    '101': '0',
    '110': '1',
    '111': '0'
}

# First line (seed)
first = '100101001101100001101000110010001000110000100'

# Red squares position
squares = [
    (2, 6), (6, 6), (12, 6),
    (10, 8),
    (24, 9),
    (36, 10),
    (14, 11),
    (31,12), 
    (7, 13), (12, 13), (26, 13),
    (40,15),
    (3, 18),
    (34, 19),
    (24,20),
    (40, 22),
    (3, 26), (13, 26),
    (32, 27),
    (23, 34),
    (33, 35),
    (12, 36)
]

# Translation table
braille = {
    '01,00,01' : 'MAJ()',
    '00,00,00' : ' ',
    '10,00,00' : 'a',
    '10,10,00' : 'b',
    '11,00,00' : 'c',
    '11,01,00' : 'd',
    '10,01,00' : 'e',
    '11,10,00' : 'f',
    '11,11,00' : 'g',
    '10,11,00' : 'h',
    '01,10,00' : 'i',
    '01,11,00' : 'j',
    '10,00,10' : 'k',
    '10,10,10' : 'l',
    '11,00,10' : 'm',
    '11,01,10' : 'n',
    '10,01,10' : 'o',
    '11,10,10' : 'p',
    '11,11,10' : 'q',
    '10,11,10' : 'r',
    '01,10,10' : 's',
    '01,11,10' : 't',
    '10,00,11' : 'u',
    '10,10,11' : 'v',
    '01,11,01' : 'w',
    '11,00,11' : 'x',
    '11,01,11' : 'y',
    '10,01,11' : 'z',
    '10,11,11' : 'à',
    '10,00,01' : 'â',
    '11,10,11' : 'ç',
    '01,10,11' : 'è',
    '11,11,11' : 'é',
    '10,10,01' : 'ê',
    '11,10,01' : 'ë',
    '11,00,01' : 'î',
    '11,11,01' : 'ï',
    '11,01,01' : 'ô',
    '01,10,01' : 'oe',
    '01,11,11' : 'ù',
    '10,01,01' : 'û',
    '10,11,01' : 'ü',
}


def evolve (row):
    """Compute next row of cellular automaton"""
    row_out = ""

    for idx in range (len (row)):
        idx_p = (idx -1) % len (row)
        idx_n = (idx +1) % len (row)
        key = row [idx_p] + row [idx] + row [idx_n]

        row_out += rule [key]
    
    return row_out


def extract_square (rows, coo):
    """Extract a red rectangle content"""
    x, y = coo [0], coo [1]
    r0 = rows [y] [x] + rows [y] [x+1]
    r1 = rows [y+1] [x] + rows [y+1] [x+1]
    r2 = rows [y+2] [x] + rows [y+2] [x+1]
    return r0 + ',' + r1 + ',' + r2

# Compute the cellular full grid
row = first
rows = []
for i in range (39):
    print (row.replace ('0', '.').replace ('1', '#'))
    rows.append (row)
    row = evolve (row)

# Extract and translate rectangles
sentence = ""
for sq in squares:    
    content = extract_square (rows, sq)
    if content in braille:
        sentence += braille [content]
    else:
        sentence += '.'
        print ("Unknown: " + content)

print (sentence)

