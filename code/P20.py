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



print ("Test encoder:")
print (encode ("Voici un tres bel exemple de phrase"))
print (encode ("Dit is een hele mooie voorbeeldzin"))


e = encode ("QUATRE JOURNAUX HOSTILES SONT PLUS A CRAINDRE QUE MILLE BAIONNETTES")
print (e)
assert (e == "34832376151972043118271517421412213528251640102218931394445362433232613344250465251383055294947535856415457")
