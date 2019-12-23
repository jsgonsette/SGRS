from Tools.vocabulary import Vocabulary

# nomenclature:
# a = corner front right up
# b = corner rear  right up
# c = corner rear  right down
# d = corner front right down
# w = corner front left  up
# x = corner rear  left  up
# y = corner rear  left  down
# z = corner front left  down
# cube = (value on face left, right, bottom, up, front, rear)


def encode (string):
    "Encode a string into multiple chained cubes"

    val = {chr (ord ('A') + i): i+1 for i in range (26)}
    cubes = []

    w = x = y = z = 0
    for i in range (len (string) // 4):
        a = ord (string [i*4]) - ord('A') +1
        b = ord (string [i*4 +1]) - ord('A') +1
        c = ord (string [i*4 +2]) - ord('A') +1
        d = ord (string [i*4 +3]) - ord('A') +1      

        side = a+b+c+d
        if i > 0:
            up= a+b+w+x
            front= a+d+w+z
            rear= b+c+x+y
            bottom= c+d+y+z
            center = up+bottom
            pside = w+x+y+z

            cube = (pside, side, bottom, up, front, rear, center)
            cubes.append (cube)

        w, x, y, z = a, b, c, d

    return cubes


def iter_face (value, fix_a=0, fix_b=0, fix_c=0, fix_d=0):
    """Iterate on all possible values of a face, given the sum 
    of the corners.
    
    value:      Sum of 4 corners
    fix_a:      Forced value on corner 'a', or 0 if free
    fix_b,c,d:  Idem

    return      yield (a, b, c, d), the 4 matching corner values
    """

    amin = 1
    amax = 26
    if fix_a: amin=amax=fix_a
    for a in range (amin, amax+1):

        bmin = max (1, value -a -26 -26)
        bmax = min (26, value -a -1 -1)
        if fix_b: 
            if fix_b < bmin or fix_b > bmax: continue
            bmin=bmax=fix_b

        for b in range (bmin,bmax+1):

            cmin = max (1, value -a -b -26)
            cmax = min (26, value -a -b -1)
            if fix_c: 
                if fix_c < cmin or fix_c > cmax: continue
                cmin=cmax=fix_c

            for c in range (cmin, cmax+1):
                
                d = value -a-b-c
                if d < 1 or d > 26: continue
                if fix_d and d != fix_d: continue
                yield (a, b, c, d)


def iter_cube (cube):
    """Iterate on all the possible corner values of a cube, given the
    number on each face"""

    (left, right, bottom, up, front, rear, center) = cube

    for (a, b, c, d) in iter_face (right):
        for (b, a, w, x) in iter_face (up, b, a):
            for (w, a, d, z) in iter_face (front, w, a, d):
                for (c, b, x, y) in iter_face (rear, c, b, x):
                
                    if bottom != d+c+y+z: continue
                    if left != x+w+y+z: continue
                    yield (a, b, c, d, w, x, y, z)


def iter_next_cube (cube, w, x, y, z):
    """Iterate on all the possible corner values of a cube, given the
    number on each face, along with the corner value of a connected face"""
    (left, right, bottom, up, front, rear, center) = cube

    for (w, x, b, a) in iter_face (up, w, x):
        for (b, x, y, c) in iter_face (rear, b, x, y):
            for (a, b, c, d) in iter_face (right, a, b, c):
                
                if bottom != d+c+y+z: continue
                if front != a+w+z+d: continue
                yield (a, b, c, d, w, x, y, z)


def decode_cubes (cubes, voc, start_msg='', last=False):

    messages = ["" for _ in range (len (cubes))]
    iterators = [None] * len (cubes)

    # Find match for first cube
    for (a, b, c, d, w, x, y, z) in iter_cube (cubes [0]):
        
        # Check the sequence make sense
        messages [0] = \
                start_msg + \
                chr (ord('A') + w-1) + chr (ord('A') + x-1) + \
                chr (ord('A') + y-1) + chr (ord('A') + z-1) + \
                chr (ord('A') + a-1) + chr (ord('A') + b-1) + \
                chr (ord('A') + c-1) + chr (ord('A') + d-1) 
        if not voc.is_valid_start (messages [0], can_extend=not last): continue

        if messages [0] == 'CRISTALD':
            print (messages [0])

        if len (cubes) == 1: 
            print (messages [0])      
            continue

        level = 1
        iterators [level] = iter_next_cube (cubes [level], a, b, c, d)

        while level > 0:
            
            if iterators [level] is None: 
                iterators [level] = iter_next_cube (cubes [level], a, b, c, d)

            try:
                (a, b, c, d, w, x, y, z) = next (iterators [level])

                # Check the sequence make sense
                messages [level] = messages [level -1] + chr (ord('A') + a-1) + chr (ord('A') + b-1) + chr (ord('A') + c-1) + chr (ord('A') + d-1) 

                if not voc.is_valid_start (messages [level]): continue
                print (messages [level])            
                
                # Continue on next cube if possble
                if level < len (cubes)-1: level += 1               

            except:
                iterators [level] = None
                messages [level] = ""
                level -= 1

                


# Check the exemple
print ("Checking example")
cubes = encode ("UNEXEMPLECUBIQUE")
for c in cubes:
    print (c)

# Check last cube
print ("LATOMIUM --> ")
cubes = encode ("LATOMIUM")
for c in cubes:
    print (c)


# Load helper for french sentence identification
WIZ_PATH = './code/Tools/libWizium.dll'
DICO_PATH = './code/Fr_Simple.txt'
DICO_PATH = './code/ODS4.txt'
voc = Vocabulary (WIZ_PATH, DICO_PATH)



# Try to decode first 3 cubes
if True:
    cubes = [(69, 77, 80, 66, 70, 76, 0), 
            (77, 45, 52, 70, 54, 68, 0),
            (45, 37, 36, 46, 45, 37, 0),
            ]

    decode_cubes (cubes, voc)

# Try to decode next 2 cubes
if False:
    cubes = [(78, 62, 78, 62, 61, 79, 0), 
            (62, 43, 58, 47, 40, 65, 0),
            ]

    decode_cubes (cubes, voc)


# Try to decode next 2 cubes
if False:
    cubes = [(49, 37, 44, 42, 46, 40, 0), 
            (37, 34, 39, 32, 47, 24, 0),
            ]

    decode_cubes (cubes, voc)

if False:
    cubes = [(48, 31, 20, 59, 26, 53, 0), 
            ]

    decode_cubes (cubes, voc)

if False:
    # This one cannot be found by this program, but the solution is "L'ATOMIUM"
    cubes = [(48, 56, 69, 35, 53, 51, 0), 
            ]

    decode_cubes (cubes, voc, last=True)