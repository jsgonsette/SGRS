def perm_i (string):
    assert (len (string) == 8)
    s = string
    output = s [5] + s [0] + s [7] + s [2] + s [1] + s [4] + s [3] + s [6]
    return output


def perm_j (string):
    assert (len (string) == 8)
    s = string
    output = s [6] + s [3] + s [0] + s [5] + s [2] + s [7] + s [4] + s [1]
    return output


# Unknown permutation for now
def perm_k (string):
    assert (len (string) == 8)
    print ("K: -> " + string)
    s = string
    output = s
    return output


def decode (string, verbose=1):

    output = ""
    while len (string) >= 9:

        # Get first letters giving permutation to apply
        modes = ""
        while (string [0] in ('i', 'j', 'k')):
            modes += string [0]
            string = string [1::]
            # break # If only one permutation allowed at a time
        assert len (modes) > 0
        modes = modes [::-1] # Reverse perm order when more than 1 ?

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

        # Extract decoded characters, but stop if new mode is given
        for idx, l in enumerate (token_plain):
            if l not in ('i', 'j', 'k'):
                output += l
            else:
                string = token_plain [idx::] + string
                break

        if verbose:
            print ("Decoding [{}] with perm {:3s} --> [{}] --> [{}]".format (token, modes, token_plain, output))

    return output, string



print (decode ("iAOPCNREIjIEOACPRNiAjCEOLiNMUIEAHETRjiCEjVPjiLEEijkRIETSiNUjUCELRQCikE1Ek"))
