#DESCRIPTOGRAFIA
palavra_descriptografada=""

alfabeto = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10,
    "K": 11, "L": 12, "M": 13, "N": 14, "O": 15, "P": 16, "Q": 17, "R": 18, "S": 19,
    "T": 20, "U": 21, "V": 22, "W": 23, "X": 24, "Y": 25, "Z": 26, " ": 0
}

#matriz codificadora inversa
Ainv=([22, -33],
      [-11, 44])

pcripto=input("Digite a palavra à ser decifrada: ")
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

C=([l1,
    l2])

#matriz P
p1=[]
p2=[]
for i in range(len(l1)):
    x = (Ainv[0][0] * l1[i]) + (Ainv[0][1] * l2[i])
    p1.append(x)
    y = (Ainv[1][0] * l1[i]) + (Ainv[1][1] * l2[i])
    p2.append(y)
P=([p1,
    p2])
print(P[0], P[1])

#pmodulo(P,27)
p1=[]
p2=[]

inversos={-1:1, -14:2, -7:4, -11:5, -4:7, -17:8, -19:10, -5:11, -25:13, -2:14, -22:16, -8:17, -10:19, -23:20, -16:22, -20:23, -13:25, -26:26}
print(inversos.keys())

for i in range(len(P[0])): #linha1 da matriz codificada 
    n = P[0][i]
    if n >= 27:
        n=n%27
    if n<0 and n>(-27):
        n=n+27
    if n <= -27:
        n=n%27
    p1.append(n)
for i in range(len(P[1])): #linha2 da matriz codificada
    n= P[1][i]
    if n >= 27:
        n=n%27
    if n<0 and n>(-27):
        n=n+27
    if n <= -27:
        n=n%27
    p2.append(n)

#matriz descodificada pós pmodulo
MP=([p1,
     p2])
print(MP)

#organização das silabas
silabas=[]
for i in range(len(p1)):
    silabas.append(p1[i])
    silabas.append(p2[i])
print(silabas)

#busca das letras no dicionário
for i in range(len(silabas)):
    valor = silabas[i]
    for key, value in alfabeto.items():
        if value == valor:
            palavra_descriptografada += key

print(palavra_descriptografada)