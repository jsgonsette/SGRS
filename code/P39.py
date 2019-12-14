def perm_i (string):
    assert (len (string) == 8)
    s = string
    output = s [1] + s [4] + s [3] + s [6] + s [5] + s [0] + s [7] + s [2]
    return output

def perm_j (string):
    assert (len (string) == 8)
    s = string
    output = s [2] + s [7] + s [4] + s [1] + s [6] + s [3] + s [0] + s [5]
    return output

print (perm_i ("AOPCNREI"))
print (perm_j ("IEOACPRN"))
print (perm_i ("AjCEOLiN"))

# i AOPCNREI
# j IEOACPRN
# i A j CEOL i NMUIEAHETR j i CE j VP ji LEE ij
# k RIETS i NU j UCELRQC ik E1E k-LkjiB-iDEjUONTE-kOjUD1MMEQNNkME-RTOikiUkEEjSkiTjTNiSE-jLOIikVANkASUIjiELESTEQU-iMTkELONDijU-kEjRBVAE1AAHDVCL-kMISNELikFALjRIkiPkiDjOEiED-ijCNkSO-iIkjiSNEYIRNikTjEMMX