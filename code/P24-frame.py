
# MIT License

# Copyright (c) [2020] [Jean-François Meessen]

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

__author__ = "Jean-François Meessen"
__year__ = 2019


import math

parts = {
'M': ('corner', (0, -1, 1), (1, -1, 1)),
'O': ('corner', (1, -1, -1), (1, 1, -1)),
'R': ('corner', (-1, 1, -1), (1, 0, -1)),
'4': ('corner', (1, -1, 0), (0, -1, 0)),
'E': ('border', (0, -1, 0), (1, -1, 1)),
'J': ('border', (-1, 1, 0), (1, -1, -1)),
'K': ('border', (1, 1, 0), (-1, 1, 1)),
'S': ('border', (-1, 0, 0), (-1, 1, 0)),
'V': ('border', (0, 1, 0), (1, -1, -1)),
'W': ('border', (-1, 0, 1), (-1, 1, 1)),
'X': ('border', (0, 1, 0), (-1, -1, 0)),
'Y': ('border', (-1, 0, 0), (0, -1, 0)),
'0': ('border', (1, 1, -1), (1, 0, -1)),
'2': ('border', (1, -1, 0), (1, 0, 0)),
'3': ('border', (-1, 1, 1), (-1, 1, -1)),
'5': ('border', (-1, 1, -1), (-1, 1, 0)),
'6': ('border', (0, 1, 0), (-1, -1, 1)),
'7': ('border', (-1, -1, 1), (0, 1, -1)),
'8': ('border', (1, -1, 0), (1, -1, 1)),
'9': ('border', (1, 0, 0), (-1, 0, 1))
}


reverse_map = {}
for key, val in parts.items():
    print(key + " => " + str(val))
    (part_type, edge1, edge2) = val 
    if edge1 in reverse_map:
        reverse_map[edge1].append((key, part_type))
    else:
        reverse_map[edge1] = [(key, part_type)]
    if edge2 in reverse_map:
        reverse_map[edge2].append((key, part_type))
    else:
        reverse_map[edge2] = [(key, part_type)]

def extend_chain(prev_chain, i, edge):
    #print("extend_chain "+str(prev_chain) + " + " + str(i))
    new_chain = prev_chain.copy()
    new_chain.append(i)
    part_type, edge1, edge2 = parts[i[0]]
    if edge == edge1:
        last_edge = edge2
    elif edge == edge2:
        last_edge = edge1
    else:
        print ("Edge is not in part "+ str(edge) + " != " + str(parts[i[0]]) )
        return
    #print("Last edge " + str(last_edge))
    next_edge = (-last_edge[0], -last_edge[1], -last_edge[2])
    next_possibilities = reverse_map[next_edge]
    #print(next_possibilities)
    for i in next_possibilities:
        if len(new_chain) >= 20 and i == new_chain[0]:
            if new_chain[5][1] == "corner" and new_chain[10][1] == "corner" and new_chain[15][1] == "corner":
                #print(str(len(new_chain)) + "Chain loop "+str(new_chain))
                print(" ".join([i[0] for i in new_chain]))
        elif i in new_chain:
            #print("Already in chain "+str(i))
            pass
        else:
            extend_chain(new_chain, i, next_edge)
    

part_chain = []
last_edge = (1, 1, -1)
extend_chain(part_chain, ('O', 'corner'), last_edge)

