
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


