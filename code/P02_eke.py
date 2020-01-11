
# MIT License

# Copyright (c) [2020] [Olivier Delbeke]

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

__author__ = "Olivier Delbeke"
__year__ = 2019


def convert(l):
    a = ord(l)-ord('A')+1
    c1 = (a-9)*(a-9)*(-6)
    c2 = ((a-9)**6) * 7
    c3 = ((a-9+7)**4) * (-3)
    o = (c1+c2+c3) % 23
    return chr(o+64)


# --------- Exploration
alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
convertis=""
for l in alphabet:
    convertis += convert(l)
print("Conversion vector : %s" % convertis)

sorties = set(convertis)
sorties.remove('@')
print(sorties)


print("----------- partie 1------")
sol1 = ""
for l in "DGWNJIEUOXEGJNI":
    sol1 += convert(l)
print("Solution 1 : %s" % sol1)

print("----------- partie 2------")
for l in "SEDTNPT":
    s = set()
    for i in range(24):
        if convertis[i]==l:
            s.add(alphabet[i])
    print(list(s))
# => solution2 = INVERSE

print("----------- partie 3------")
for l in sorties:
    c, r = l, l
    for i in range(20):
        n = convert(c)
        r += n
        c = n
    print(r)
# => solution2 = TOURNE


