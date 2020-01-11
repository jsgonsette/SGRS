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


def perm_i (string):
    assert (len (string) == 8)
    s = string
    output = s [5] + s [0] + s [7] + s [2] + s [1] + s [4] + s [3] + s [6]
    return output

def perm_i_inv (string):
    assert (len (string) == 8)
    s = string
    output = s [1] + s [4] + s [3] + s [6] + s [5] + s [0] + s [7] + s [2]
    return output

def perm_j (string):
    assert (len (string) == 8)
    s = string
    output = s [6] + s [3] + s [0] + s [5] + s [2] + s [7] + s [4] + s [1]
    return output

def perm_j_inv (string):
    assert (len (string) == 8)
    s = string
    output = s [2] + s [7] + s [4] + s [1] + s [6] + s [3] + s [0] + s [5]
    return output

# Assume pk(pj(pi)) == identity, which seems correct
def perm_k (string):
    assert (len (string) == 8)
    s = string
    output = s [7] + s [6] + s [1] + s [0] + s [3] + s [2] + s [5] + s [4]
    # output = s [3] + s [2] + s [5] + s [4] + s [7] + s [6] + s [1] + s [0]
    return output

def perm_k_inv (string):
    assert (len (string) == 8)
    s = string
    output = s [3] + s [2] + s [5] + s [4] + s [7] + s [6] + s [1] + s [0]
    return output


def decode (string, verbose=1):

    output = ""
    while len (string) >= 9:

        # Get first letters giving permutation to apply (we can get multiple permutations in a row) 
        # We also have to deal with the minus sign for the inverse permutations (-i, -j, -k), along with the -1 permutation
        # For code simpliciy, -i is called x and -j -> y and -k ->z and -1 -> w
        modes = ""
        while (string [0] in ('i', 'j', 'k', '-', '1')):

            if string [0] == '-': 
                permtype = string [1]
                assert permtype in ('1', 'i', 'j', 'k')
                if permtype == 'i': permtype = 'x'
                elif permtype == 'j': permtype = 'y'
                elif permtype == 'k': permtype = 'z'
                elif permtype == '1': permtype = 'w'
                string = permtype + string [2::]

            modes += string [0]
            string = string [1::]
        assert len (modes) > 0

        # Decode 8 characters with the correct permutation
        # (maybe multiple times, as instructed)
        token = string [0:8]
        string = string [8::]
        token_plain = token
        for mode in modes:
            if mode == 'i':
                token_plain = perm_i (token_plain)
            elif mode =='j':
                token_plain = perm_j (token_plain)
            elif mode =='k':
                token_plain = perm_k (token_plain)
            elif mode == 'w':
                token_plain = token_plain [4:8] + token_plain [0:4]
            if mode == 'x':
                token_plain = perm_i_inv (token_plain)
            elif mode =='y':
                token_plain = perm_j_inv (token_plain)
            elif mode =='z':
                token_plain = perm_k_inv (token_plain)
            elif mode =='1':
                pass

        # Extract decoded characters, but stop if new mode is given
        for idx, l in enumerate (token_plain):
            if l not in ('i', 'j', 'k', '-', '1'):
                output += l
            else:
                string = token_plain [idx::] + string
                break

        if verbose:
            print ("Decoding [{}] with perm {:3s} --> [{}] --> [{}]".format (token, modes, token_plain, output))

    return output, string


# Juste check our permutation are correct
print (perm_i (perm_i_inv ("12345678")))
print (perm_j (perm_j_inv ("12345678")))
print (perm_k (perm_k_inv ("12345678")))
print (perm_k (perm_j (perm_i ("12345678"))))

# Decode this damn @#!& string
print (decode ("iAOPCNREIjIEOACPRNiAjCEOLiNMUIEAHETRjiCEjVPjiLEEijkRIETSiNUjUCELRQCikE1Ek-LkjiB-iDEjUONTE-kOjUD1MMEQNNkME-RTOikiUkEEjSkiTjTNiSE-jLOIikVANkASUIjiELESTEQU-iMTkELONDijU-kEjRBVAE1AAHDVCL-kMISNELikFALjRIkiPkiDjOEiED-ijCNkSO-iIkjiSNEYIRNikTjEMMX?"))
