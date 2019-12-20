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
f = Image.open ("wiki/41-Morse.png")
width, height = f.size

raw = f.tobytes ()
raw = np.reshape (np.array ([b for b in raw]), [height, -1])


# Scan all lines in the picture, ignore duplicates
coded_lines = []
prev = []
for y in range (height):
    code = scan_line (raw [y,:])
    if len (code) == 0 and len (prev) > 0:
        coded_lines.append (prev)
    prev = code

# We have got a big vector with 4 possibles values (dot, bar, seperator, word seperator)
message = decode_morse (coded_lines)
print (message)

