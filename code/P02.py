
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

def print_alphabet ():

    encoding = {chr (ord ('a') + i): chr (ord ('a') + encode (i+1)-1) for i in range (26)}
    # decoding = {encoding [l]: l for l in encoding}

    for k in encoding:
        print (k + ' --> ' + encoding [k])


print_alphabet ()
print (encode_string ('DGWNJIEUOXEGJNI'))

