
zero  = set( ['a','b','c','e','g','f'] )
one   = set( ['c','g'] )
two   = set( ['a','c','d','e','f'] )
three = set( ['a','c','d','g','f'] )
four  = set( ['b','c','d','g'] )
five  = set( ['a','b','d','g','f'] )
six   = set( ['a','b','d','g','f','e'] )
seven = set( ['a','c','g'] )
eight = set( ['a','b','c','d','e','f','g'] )
nine  = set( ['a','b','c','d','g','f'] )
codes = [ zero, one, two, three, four, five, six, seven, eight, nine ]

# Get possibilities ( chiffre1, max changements, alumettes dispo )
# -> [ (4,2), (5,3) ]  # 4 en deux mouvements, 
# manque le solde en alumettes
def get_changes( a, b ):
    common = len(codes[a].intersection(codes[b]))
    missing = len(codes[b]-codes[a])
    excess = len(codes[a]-codes[b])
    if excess >= missing:
        movable = missing
        external = 0
    else:
        movable = excess
        external = missing - movable
    # Count as movement :number of internal movements + number of additional matches needed
    movements = movable + external
    saldo = excess - missing # Correct
    #print("From %d to %d : %d moved internally, %d saldo, %d movements" % (a,b,movable,saldo,movements))
    return (saldo, movements)

#get_changes(2,1)
#get_changes(3,9)
#get_changes(5,7)
#get_changes(2,2)
#exit()

for sign in [0, -1]:
    if sign==0:
        current_saldo, movements_left = 0, 4
    else:
        current_saldo, movements_left = 1, 4
    for c1 in range(10):
        saldo1, movements1 = get_changes(2 , c1)
        if movements1 > movements_left:
            continue
        current_saldo += saldo1
        movements_left -= movements1
        for c2 in range(10):
            saldo2, movements2 = get_changes(3 , c2)
            if movements2 > movements_left:
                continue
            current_saldo += saldo2
            movements_left -= movements2
            for c3 in range(10):
                saldo3, movements3 = get_changes(5 , c3)
                if movements3 > movements_left:
                    continue
                current_saldo += saldo3
                movements_left -= movements3
                for c4 in range(10):
                    saldo4, movements4 = get_changes(2 , c4)
                    # Exactly 4 movements
                    if movements4 != movements_left:
                        continue
                    # Saldo must be 0
                    if current_saldo + saldo4 != 0:
                        continue
                    # Calculus must match
                    if sign==0 and 10*c1+1 + c2 == 10*c3 + c4:
                        print("%d + %d = %d" % (10*c1+1,c2,10*c3+c4))
                    if sign!=0 and 10*c1+1 - c2 == 10*c3 + c4:
                        print("%d - %d = %d" % (10*c1+1,c2,10*c3+c4))
                current_saldo -= saldo3
                movements_left += movements3
            current_saldo -= saldo2
            movements_left += movements2
        current_saldo -= saldo1
        movements_left += movements1

# 21 + 2 = 23
# 21 + 7 = 28
# 31 + 2 = 33
# 31 + 7 = 38
# 51 + 2 = 53
# 51 + 7 = 58
# 31 - 9 = 22
# 71 - 3 = 68
# 81 - 9 = 72 --- solution

