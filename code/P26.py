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


N = 100

for u in range (-N,N+1,2):
    print ("search u = " + str (u))
    n=1-u
    e=(1-n)//2
    l=-n-u
    f=9-n-e-u

    maxi = max ([u,n,e,l,f])
    mini = min ([u,n,e,l,f])
    if maxi-mini > 60: continue

    for z in range (-N,N+1):
        s=6-z-e
        v=7-z-n-2*e

        maxi = max ([u,n,e,l,f,z,s,v])
        mini = min ([u,n,e,l,f,z,s,v])
        if maxi-mini > 60: continue

        for i in range (-N,N+1):
            x=6-s-i
            r=4-v-i-e
            d=3-r-i-e

            if d != 2-e-u-x: continue

            o = -z-e-r
            t=3-r-o-i-s
            h=8-u-i-t

            maxi = max ([u,n,e,l,f,z,s,v,i,x,r,d,o,t,h])
            mini = min ([u,n,e,l,f,z,s,v,i,x,r,d,o,t,h])
            if maxi-mini > 60: continue

            a = (7-h-t-t+i+n-u-r-e)
            if a % 2 == 1: continue
            a = a//2

            c=8-a-h-t
            q=5-c-i-n

            maxi = max ([a,c,d,e,f,h,i,l,n,o,q,r,s,t,u,v,x,z])
            mini = min ([a,c,d,e,f,h,i,l,n,o,q,r,s,t,u,v,x,z])
            if maxi-mini > 60: continue

            assert (q==4-u-a-t-r-e)
            break    

        if i == N: continue
        else: break

    if z == N: continue
    else: break

if u == N:
    print ("FAILED")
    exit ()

j = 5-v-i-f
g = 9-n-e-e-n
p = 7-s-e-t
w = 2-t-e-e

print ("NUL=" + str (n+u+l))
print ("ZERO=" + str (z+e+r+o))
print ("EEN=" + str (e+e+n))
print ("UN=" + str (u+n))
print ("TWEE=" + str (t+w+e+e))
print ("DEUX=" + str (d+e+u+x))
print ("DRIE=" + str (d+r+i+e))
print ("TROIS=" + str (t+r+o+i+s))
print ("VIER=" + str (v+i+e+r))
print ("QUATRE=" + str (q+u+a+t+r+e))
print ("VIJF=" + str (v+i+j+f))
print ("CINQ=" + str (c+i+n+q))
print ("ZES=" + str (z+e+s))
print ("SIX=" + str (s+i+x))
print ("ZEVEN=" + str (z+e+v+e+n))
print ("SEPT=" + str (s+e+p+t))
print ("ACHT=" + str (a+c+h+t))
print ("HUIT=" + str (h+u+i+t))
print ("NEGEN=" + str (n+e+g+e+n))
print ("NEUF=" + str (n+e+u+f))

print ("TIEN=" + str (t+i+e+n))
print ("ELF=" + str (e+l+f))
print ("TWAALF=" + str (t+w+a+a+l+f))
print ("DIX=" + str (d+i+x))
print ("ONZE=" + str (o+n+z+e))
print ("DOUZE=" + str (d+o+u+z+e))

maxi = max ([a,c,d,e,f,g,h,i,j,l,n,o,p,q,r,s,t,u,v,w,x,z])
mini = min ([a,c,d,e,f,g,h,i,j,l,n,o,p,q,r,s,t,u,v,w,x,z])

print ("Delta="+str (maxi-mini))