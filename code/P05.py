
import numpy as np 

# digit representation by listing the numbers corresponding to ON segments
digits = {
    'A': [1,2,3,4,7,9,10,12],
    'B': [1,2,4,5,6,8,9,11,12],
    'C': [1,2,5,6,7,10],
    'D': [1,2,5,6,8,9,11,12],
    'E': [1,2,3,5,6,7,10],
    'F': [1,2,3,7,10],
    'G': [1,2,4,5,6,7,10,12],
    'H': [3,4,7,9,10,12],
    'I': [1,2,5,6,8,11],
    'J': [5,6,9,10,12],
    'j': [5,8,10,11],
    'K': [3,7,10,14,16],
    'L': [5,6,7,10],
    'M': [7,9,10,12,13,14],
    'N': [7,9,10,12,13,16],
    'O': [1,2,5,6,7,9,10,12],
    'P': [1,2,3,4,7,9,10],
    'Q': [1,2,5,6,7,9,10,12,16],
    'R': [1,2,3,4,7,9,10,16],
    'S': [1,2,3,4,5,6,7,12],
    'T': [1,2,8,11],
    'U': [5,6,7,9,10,12],
    'V': [7,10,14,15],
    'W': [7,9,10,12,15,16],
    'X': [13,14,15,16],
    'Y': [3,4,5,6,7,9,12],
    'Z': [1,2,5,6,14,15],
    '?': [1,2,4,9,11],
    '!': [9,12],
    ' ': [],
    '-': [3,4],
    '0': [1,2,5,6,7,9,10,12,14,15],
    '1': [9,12,14],
    '2': [1,2,3,4,5,6,9,10],
    '3': [1,2,3,4,5,6,9,12],
}

coded = [
    '01-02-03-04-07-08-09-10-11-12',
    '',
    '05-06-09-12',
    '01-02-03-05-06-07-10',
    '08-09-11-12',
    '03-04-05-06-07-10',
    '03-07-08-10-11',
    '01-02-04-05-06-07-10-12',
    '08-11',
    '01-02-03-05-06-09-12-14-15',
    '03-04-10-12',
    '01-02-04-08-09-11-12',
    '15',
    '01-02-07-10',
    '03-04-05-06-07-08-09-10-11-12',
    '05-06-07-10-14-15',
    '01-02-03-05-06-09-12-15-16',
    '01-02-03-04-07-09-10-12',
    '01-02-03-04-12',
    '01-02-04-07-09',
    '',
    '05-06-09-12',
    '01-02-04-05-06-09-12',
    '01-02-03-04-07-09-10-12',
    '01-02-03-05-06-07-10',
    '01-02-04-07-10-14-15',
    '03-04-08-09-10-11',
    '04-05-06-09-10-12-15',
    '01-02-03-04-05-06-07-12',
    '01-02-08-09-11-12',  
]

def flip_horizontal (digit):
    in_ons = [False] + [i in digit for i in range (1,17)]
    out_ons = list (in_ons)

    out_ons [1] = in_ons [2]
    out_ons [2] = in_ons [1]

    out_ons [3] = in_ons [4]
    out_ons [4] = in_ons [3]

    out_ons [5] = in_ons [6]
    out_ons [6] = in_ons [5]

    out_ons [7] = in_ons [9]
    out_ons [9] = in_ons [7]

    out_ons [10] = in_ons [12]
    out_ons [12] = in_ons [10]

    out_ons [13] = in_ons [14]
    out_ons [14] = in_ons [13]

    out_ons [15] = in_ons [16]
    out_ons [16] = in_ons [15]

    segs = list ([i[0] for i in np.argwhere (out_ons)])
    return segs


def flip_vertical (digit):
    in_ons = [False] + [i in digit for i in range (1,17)]
    out_ons = list (in_ons)

    out_ons [1] = in_ons [5]
    out_ons [5] = in_ons [1]

    out_ons [2] = in_ons [6]
    out_ons [6] = in_ons [2]

    out_ons [7] = in_ons [10]
    out_ons [10] = in_ons [7]

    out_ons [9] = in_ons [12]
    out_ons [12] = in_ons [9]

    out_ons [8] = in_ons [11]
    out_ons [11] = in_ons [8]

    out_ons [13] = in_ons [15]
    out_ons [15] = in_ons [13]

    out_ons [14] = in_ons [16]
    out_ons [16] = in_ons [14]

    segs = list ([i[0] for i in np.argwhere (out_ons)])
    return segs


def combine (digit_left, digit_right):

    out_ons = [False] * 17

    for i in range (1,17):
        out_ons [i] = ((i in digit_left) and (i not in digit_right)) or ((i not in digit_left) and (i in digit_right))

    digit_out = list ([i[0] for i in np.argwhere (out_ons)])
    return digit_out


def make_digit_string (digit):
    """Return a string with a unique encoding of the digits.
    if digits 3,7,12 and 11 are on, the output is '03-07-11-12'
    """
    return "-".join (["{:02d}".format (i) for i in sorted (digit)])


def display_comb (combinations, coded_digit):
    if coded_digit in combinations:
        print (combinations [coded_digit])
    else:
        print ("No combination found")


def print_matches ():
    # pre compute flips of all digits
    lefts = {key:flip_horizontal (digits [key]) for key in digits}
    rights = {key:flip_vertical (digits [key]) for key in digits}

    # Combine them all together and store all the results
    combinations = {}

    for kl in lefts:
        dl = lefts [kl]
        for kr in rights:
            dr = rights [kr]
            
            # Combination of both digits
            combi = combine (dl, dr)

            # Store {output digit -> "digit left"+"digit right"}
            key = make_digit_string (combi)

            if key not in combinations:
                combinations [key] = kl + kr
            else:
                combinations [key] += '/' + kl+kr
            
    # Display possibilities for each position
    for c in coded:
        display_comb (combinations, c)


def try_message (line1, line2):
    for s1, s2, c in zip (line1, line2, coded):

        digit_left = digits [s1]
        digit_right = digits [s2]        
        digit_out = combine (flip_horizontal (digit_left), flip_vertical (digit_right))
        out_str = make_digit_string (digit_out)
        status = " OK " if out_str == c else "WRNG"

        print ("[" + status + "]" + s1 + " + " + s2 + " --> " + out_str)


# Help to find a solution
print ("All combinations at each position:")
print ("-"*20)
print_matches ()

# Solution
print ("\n\nPartial solution for now:")
print ("-"*20)
try_message ("INTELLIGENCE- ALWAYS THE FIRST", "AND THE BEST LINE OF DEFENSE !")


