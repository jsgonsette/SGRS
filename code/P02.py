

def encode (number):
    n = number    
    sum = ((n-9)**6)*7 + ((n-2)**4)*(-3) + ((n-9)**2)*(-6)
    return sum % 23

def encode_string (string):

    string = string.lower ()
    code = [encode (ord (s) - ord ('a') + 1) for s in string]

    output = ''
    for c in code:
        output += chr (c + ord ('a') -1)

    return output

def decode_string (string):

    encoding = {chr (ord ('a') + i): chr (ord ('a') + encode (i+1)-1) for i in range (26)}
    # decoding = {encoding [l]: l for l in encoding}

    for k in encoding:
        print (k + ' --> ' + encoding [k])


print (encode_string ('DGWNJIEUOXEGJNI'))
# https://www.crazy-numbers.com/en/33418

