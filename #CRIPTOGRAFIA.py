#CRIPTOGRAFIA 
palavra_criptografada=""

alfabeto = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10,
    "K": 11, "L": 12, "M": 13, "N": 14, "O": 15, "P": 16, "Q": 17, "R": 18, "S": 19,
    "T": 20, "U": 21, "V": 22, "W": 23, "X": 24, "Y": 25, " ":0, "Z": 26
}
print(alfabeto.keys())
#para pegar o valor da letra: alfabeto["letra"]

#matriz codificadora
A=([4, 3],
   [1, 2])

#string a ser decodificada
nome=input("Digite a palavra a ser codificada: ").upper()
l1=[]
l2=[]

cont=0 #variavel cont aumenta de 1 em 1 é usada no if para alternar as listas em que se insere o valor das letras
for i in range(len(nome)):
    cont+=1
    letra=nome[i]
    chave=letra
    x=alfabeto[chave]
    print(f"{nome[i]}->{alfabeto[chave]}")
    if cont % 2 != 0:
        l1.append(x)
    else:
        l2.append(x)
if len(l2) < len(l1):
    ultimoelemento=l1[len(l1)-1]
    l2.append(ultimoelemento)
#matriz P da palavra a ser codificada
P=([l1,
    l2])
print(P)

#matriz codificada
c1=[]
c2=[]
for i in range(len(l1)):
   x = (A[0][0] * l1[i]) + (A[0][1] * l2[i])
   c1.append(x)
   y = (A[1][0] * l1[i]) + (A[1][1] * l2[i])
   c2.append(y)
C=([c1,
    c2])

print(f"{A}x{P}={C}")

#pmodulo(C,27)
C1=[]
C2=[]
for i in range(len(C[0])): #linha1 da matriz codificada 
    n = C[0][i]
    if n >= 27:
        n=n%27
    C1.append(n)
for i in range(len(C[1])): #linha2 da matriz codificada
    n= C[1][i]
    if n>= 27:
        n=n%27
    C2.append(n)

#matriz codificada pós pmodulo
MC=[[C1, 
     C2]]
print(MC)

#organização dos valores das silabas
silabas=[]
for i in range(len(C1)):
    silabas.append(C1[i])
    silabas.append(C2[i])

#busca no dicionário as chaves(letras) equivalentes aos valores da letras codificadas
for i in range(len(silabas)):
    valor=silabas[i]
    for key, value in alfabeto.items():
        if value == valor:
            palavra_criptografada += key

print(palavra_criptografada)