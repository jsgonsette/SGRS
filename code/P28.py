def gen_sequence (n):

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
    
    table = list (gen_sequence (200))
    encoded = []
    pos = 0
    while integer >= 1:
        on = integer & 1
        if on: encoded.append (table [pos])
        integer //= 2
        pos += 1

    return encoded

def decode (coded_list):

    table = list (gen_sequence (200))

    integer = 0
    weight = 1
    pos = 0
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
print (decode (coded))