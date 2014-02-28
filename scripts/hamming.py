import binascii

def hammingDistance(byteArr1, byteArr2):
    #print binascii.hexlify(byteArr1)
    #print binascii.hexlify(byteArr2)
    if(len(byteArr1) != len(byteArr2)):
        raise ValueError("Undefined for sequences of unequal length")

    hammDist = 0
    for i in range(0, len(byteArr1)):
        for j in range(0, 8):
            bit1 = byteArr1[i] & (1 << j)
            bit2 = byteArr2[i] & (1 << j)
            if( bit1 != bit2 ):
                hammDist += 1

    #print hammDist
    return hammDist

