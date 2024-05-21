#DESCRIPTOGRAFIA
import numpy as np


alfabeto = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10,
    "K": 11, "L": 12, "M": 13, "N": 14, "O": 15, "P": 16, "Q": 17, "R": 18, "S": 19,
    "T": 20, "U": 21, "V": 22, "W": 23, "X": 24, "Y": 25, "Z": 0
}

#matriz codificadora inversa
Ainv=np.array([[42, -63],
              [-21, 84]])

pcripto='CGOPYFCOZJ'
l1=[]
l2=[]

cont=0
for i in range(len(pcripto)):
    cont+=1
    letra=pcripto[i]
    chave=letra
    x=alfabeto[chave]
    print(f"{pcripto[i]}->{x}")
    if cont%2!=0:
        l1.append(x)
    else:
        l2.append(x)
if len(l2)<len(l1):
    ultimoelemento=l1[len(l1)-1]
    l2.append(ultimoelemento)
print(f"{l1}\n{l2}")

C=np.array([[l1,
             l2]])

P=Ainv @ C
print(P)

#pmodulo(P,26)
p1=[]
p2=[]

inversos={-1:1, -9:3, -21:5, -15:7, -3:9, -19:11, -7:15, -23:17, -11:19, -5:21, -17:23, -25:25}
print(inversos.keys())

for i in range(len(P[0])): #linha1 da matriz codificada 
    n = P[0][i]
    if n >= 26 and n > 0:
        n=n%26
    if n<0 and n>(-26):
        for chave, valor in inversos.items():
            if chave == n:
                n=valor
                print(valor)
    if n <= -26:
        n = 26 + (n%26)
    p1.append(n)
for i in range(len(P[1])): #linha2 da matriz codificada
    n= P[1][i]
    if n >= 26:
        n=n%26
    p2.append(n)

MP=([p1,
    p2])

print(MP)