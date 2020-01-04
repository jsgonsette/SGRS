
import Tools.ciphers as ciphers

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


def grid_rot (grid, shift):
    new_grid = []
    for line in grid:
        new_line = ''
        for s in line:
            if s == '-': new_line += '-'
            elif s == ' ': new_line += ' '
            else: new_line += ciphers.rotate (s, shift)
        new_grid.append (new_line)

    return new_grid

def grid_print (grid):
    for line in grid:
        print (' '.join (line))


for shift in range (1,26):
    print ("\nRotation " + str (shift))
    grid_print (grid_rot (grid, shift))


