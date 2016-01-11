Hit_Count = 0
n = 20
Trade_Count = Range("ZZ1").End(xlToLeft).Column - 13

for j in range(0,n-1)
    for i in range(0,n-1)
        if last_price < tgt:
            last_price = i
                for k in range(i,n)
                    Range("M1").Offset(k + 1, j) = ""
            Hit_Count = Hit_Count + 1
        else:
            Range("M1").Offset(i, j) = ""

First_Hit = Hit_Count / Trade_Count