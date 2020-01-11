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


# LES VALEURS EN GRIS 
# SONT EGALEMENT EN CODE MORSE

from PIL import Image
import numpy as np

morse = {
    '01': 'A',
    '1000': 'B',
    '1010': 'C',
    '100': 'D',
    '0': 'E',
    '0010': 'F',
    '110': 'G',
    '0000': 'H',
    '00': 'I',
    '0111': 'J',
    '101': 'K',
    '0100': 'L',
    '11': 'M',
    '10': 'N',
    '111': 'O',
    '0110': 'P',
    '1101': 'Q',
    '010': 'R',
    '000': 'S',
    '1': 'T',
    '001': 'U',
    '0001': 'V',
    '011': 'W',
    '1001': 'X',
    '1011': 'Y',
    '1100': 'Z',
}


def scan_line (values):
    """Scan a line of pixel and extract pixel values, ignoring duplicates, using 255 (white) as seperator"""
    code = []
    prev = 255
    for v in values:
        if v == 255 and prev != 255:
            code.append (prev)
        prev = v
        
    return code


def decode_morse (values):
    """Decode the message assuming 32 is a dot, 96 is a bar, 159 is seperator and 232 is word seperator"""

    message = ''
    values = np.reshape (np.array (values), [-1])
    raw = ''
    for v in values:
        if v == 32: raw += '0'
        elif v == 96: raw += '1'
        elif v == 159 or v == 223:
            if len (raw):
                message += morse [raw]
            else:
                message += '\n'
            raw = ''
            if v == 223:
                message += ' '
        else:
            print ("HAAAARG")
            
    return message



# Open the image and load it into a numpy array
print ("\nLoad PNG screenshot ...")
f = Image.open ("wiki/41-Morse.png")
width, height = f.size

raw = f.tobytes ()
raw = np.reshape (np.array ([b for b in raw]), [height, -1])


# Scan all lines in the picture, ignore duplicates
print ("\nScan screenshot and make a grey level table ...")
coded_lines = []
prev = []
for y in range (height):
    code = scan_line (raw [y,:])
    if len (code) == 0 and len (prev) > 0:
        coded_lines.append (prev)
    prev = code

# We have got a big vector with 4 possibles values (dot, bar, seperator, word seperator)
print ("\nDecoding ...")
message = decode_morse (coded_lines)

print ("\nFinal message:")
print (message)

