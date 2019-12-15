import numpy as np


frequencies = {
    'A': 0.0840,
    'B': 0.0106,
    'C': 0.0303,
    'D': 0.0418,
    'E': 0.1726,
    'F': 0.0112,
    'G': 0.0127,
    'H': 0.0092,
    'I': 0.0734,
    'J': 0.0031,
    'K': 0.0005,
    'L': 0.0601,
    'M': 0.0296,
    'N': 0.0713,
    'O': 0.0526,
    'P': 0.0301,
    'Q': 0.0099,
    'R': 0.0655,
    'S': 0.0808,
    'T': 0.0707,
    'U': 0.0574,
    'V': 0.0132,
    'W': 0.0004,
    'X': 0.0045,
    'Y': 0.0030,
    'Z': 0.0012,
}

numbers1 = [3,48,32,37,6,15,19,7,20,43,11,8,27,1,5,17,42,14,12,21,35,28,25,16,40,10,22,18,9,31,39,44,45,36,24,33,23,26,13,34,4,2,50,46,52,51,38,30,55,29,49,47,53,58,56,41,54,57]
numbers2 = [3,48,32,37,6,15,19,7,20,43,11,8,27,1,5,17,4,2,14,12,21,35,28,25,16,40,10,22,18,9,31,39,44,45,36,24,33,23,26,13,34,42,50,46,52,51,38,30,55,29,49,47,53,58,56,41,54,57]
numbers3 = [3,48,32,37,6,1,5,19,7,20,43,11,8,27,15,17,42,14,12,21,35,28,25,16,40,10,22,18,9,31,39,44,45,36,24,33,23,26,13,34,4,2,50,46,52,51,38,30,55,29,49,47,53,58,56,41,54,57]
numbers4 = [3,48,32,37,6,1,5,19,7,20,43,11,8,27,15,17,4,2,14,12,21,35,28,25,16,40,10,22,18,9,31,39,44,45,36,24,33,23,26,13,34,42,50,46,52,51,38,30,55,29,49,47,53,58,56,41,54,57]

def encode (string):

    output = ""    
    string = string.upper ()
    encoder = {}
    skip = 0

    for index, s in enumerate (string):
        letter = ord (s) - ord ('A')
        if letter < 0 or letter >= 26: 
            skip += 1
            continue

        index -= skip
        if s not in encoder:
            encoder [s] = [index+1]
        else:
            encoder [s].append (index+1)

    empty = False
    while empty == False:

        empty = True
        for index in range (26):
            letter = chr (index + ord ('A'))
            if letter in encoder:
                output += str (encoder [letter][0])
                del encoder [letter][0]
                if not len (encoder [letter]): del encoder [letter]
                empty = False

    return output

def segment_code (code_string):
    return None


def get_promisings (letter_probas):

    distrib = [(f, chr (i + ord('A'))) for i, f in enumerate (letter_probas)]
    distrib = sorted (distrib, key=lambda x: x [0], reverse=True)
    max_f = distrib [0][0]
    idx = 1
    while distrib [idx][0] > max_f/20: idx += 1    
    return [l for f, l in distrib [0:idx]]

def decode (numbers, probas):
    num_letters = len (numbers)
    original = [[] for _ in range (num_letters)]

    for idx, n in enumerate (numbers):
        
        letter_probas = probas [idx]
        promising = get_promisings (letter_probas)        
        original [n-1] = promising

    print ("")


def estimate_proba (length):
    """Estimate the probability distribution of letters at each position along the sentence"""

    probas = np.zeros ([length, 26])

    letters = [chr (ord ('A') + i) for i in range (26)]
    letter_probas = [frequencies [chr (ord ('A') + i)] for i in range (26)]
    letter_probas [-1] = 1 - sum (letter_probas [0:25])

    np.random.seed (1)

    # Monte Carlo estimation
    for i in range (1000):
        # Take sentence at random, with french frequencies, and sort letters
        sentence = list (sorted (np.random.choice (letters, length, p=letter_probas)))

        prev_letter = next_letter = ' '
        position = idx = 0
        while len (sentence):
            
            # Extract next letter (must be different from previous)
            while idx < len (sentence):
                next_letter = sentence [idx]
                if next_letter != prev_letter:
                    del sentence [idx]
                    break
                else: idx += 1
            # Detect when we have to restart (next row in encoding)
            if next_letter == prev_letter or next_letter == ' ':
                prev_letter = ' '
                idx = 0
                continue

            # Count this letter at current position
            idx_letter = ord (next_letter) - ord ('A')
            probas [position, idx_letter] += 1

            # Move on
            position += 1
            prev_letter = next_letter
            next_letter = ' '
            
    probas /= (i+1)
    return probas


print ("Test encoder:")
print (encode ("Voici un tres bel exemple de phrase"))
print (encode ("Dit is een hele mooie voorbeeldzin"))

probas = estimate_proba (len (numbers1))
decode (numbers1, probas)
# decode (numbers1)


