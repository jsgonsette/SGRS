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



print ("Test encoder on:")
msg = "Voici un tres bel exemple de phrase"
print (msg)
print (encode (msg))

msg = "Dit is een hele mooie voorbeeldzin"
print (msg)
print (encode (msg))

msg = "QUATRE JOURNAUX HOSTILES SONT PLUS A CRAINDRE QUE MILLE BAIONNETTES"
e = encode (msg)
print ("\nTest encoding on:")
print (msg)
print (e)
assert (e == "34832376151972043118271517421412213528251640102218931394445362433232613344250465251383055294947535856415457")
