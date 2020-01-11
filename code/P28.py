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
__year__ = 2020


def gen_sequence (n):
    """Generate the tuple corresponding to a number n"""

    yield []
    seq = [0]
    
    for _ in range (n-1):
        yield list (seq)

        # First rule, increase length by adding a zero, if possible
        if seq [0] != 0:
            seq = [0] + seq

        # Otherwise we start from the left, looking for the first digit we can increase
        # and drop everything on the left
        else:
            success = False
            for i in range (0, len (seq)-1):
                if seq [i] < seq [i+1]-1:
                    seq [i] = seq [i]+1
                    seq = seq [i:]
                    success = True
                    break

            if not success: seq = [seq [-1] +1]

def encode (integer):
    """Encode an integer"""
    
    # Make a table with the first 200 tuples
    table = list (gen_sequence (200))
    
    # Add each tuple corresponding to all bit at 1
    encoded = []
    pos = 0
    while integer >= 1:
        on = integer & 1
        if on: encoded.append (table [pos])
        integer //= 2
        pos += 1

    return encoded


def decode (coded_list):
    """Decode a sequence of tuple to find out the integer"""

    # Encode the first 200 bits
    table = list (gen_sequence (200))

    integer = 0
    weight = 1
    pos = 0

    # Build the number by adding all the matching bits
    for item in coded_list:
        while table [pos] != item:
            weight *= 2
            pos += 1

        integer += weight

    return integer


print ("Check encoding is correct")
print ('-'*20)
print ("15 --> " + str (encode (15)))
print ("35 --> " + str (encode (35)))
print ("256 --> " + str (encode (256)))
print ("616 --> " + str (encode (616)))
print ("1999 --> " + str (encode (1999)))
print ("2048 --> " + str (encode (2048)))
print ("13109 --> " + str (encode (13109)))
print ("4997971 --> " + str (encode (4997971)))
print ("327547040565 --> " + str (encode (327547040565)))


coded = [[],
      [0,2],[3],[0,2,3],[4],[0,2,4],[0,2,3,4],[1,5],[2,5],[0,2,5],
    [1,2,5],[3,5],[0,3,5],[1,3,5],[0,1,3,5],[0,2,3,5],[1,2,3,5],
    [0,4,5],[2,4,5],[0,2,4,5],[1,2,4,5],[0,3,4,5],[0,2,3,4,5],
    [1,2,3,4,5],[6],[0,2,6],[1,2,6],[0,3,6],[1,3,6],[1,2,3,6],
    [0,2,4,6],[1,3,4,6],[0,2,3,4,6],[1,2,3,4,6],[0,5,6],[2,5,6],
    [0,2,5,6],[1,2,5,6],[3,5,6],[0,2,3,5,6],[1,2,3,5,6],[0,4,5,6],
    [1,4,5,6],[0,1,4,5,6],[0,2,4,5,6],[1,2,4,5,6],[0,3,4,5,6],
    [2,3,4,5,6],[0,2,3,4,5,6],[1,2,3,4,5,6],[7],[1,7],[0,2,7],
    [1,2,7],[0,3,7],[1,2,3,7],[0,2,4,7],[3,4,7],[0,2,3,4,7],
    [5,7],[0,2,5,7],[3,5,7],[0,2,3,5,7]
]

print ("\nMysterious number:")
decoded = decode (coded)
print (decoded)

print ("In hex and binary:")
print (hex (decoded))
print (bin (decoded))

print ("In hex, it's clear that we have a message in ASCII. Let's decode it")
line = ''
while decoded > 0:
    line = chr (decoded % 256) + line
    decoded //= 256

print (line)