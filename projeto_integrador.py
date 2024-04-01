import pandas as pd 
from tabulate import tabulate

#Leitura dos dados:
cod_prod=int(input("Digite o código do produto: "))
nome_prod=str(input("Digite o nome do produto: "))
descrição=str(input("Descreva o produto: "))
CP=float(input("Digite o custo do produto: "))
CF=float(input("Digite o custo fixo/adiministrativo: "))
CV=float(input("Digite a comissão de venda: "))
IV=float(input("Digite os impostos sobre a venda: "))
ML=float(input("Digite a margem de lucro desejada: "))

#Calculo do preço de venda:
PV = CP/(1-((CF+CV+IV+ML)/100))
#################################


#Custo de aquisição:
PCA=(CP*100)//PV
#Receita bruta:
RB=PV-CP
PRB=100-PCA
#Custofixo:
PCF=(CF*PRB)//RB
#Comissão
VCV=(CV*RB)//PRB
#ValorImposto
VI=(IV*RB)//PRB
#OutrosCustos
OC=CF+VCV+VI
POC=(OC*PRB)//RB
#Rentabilidade
R=RB-OC


tabela = [
    ["Descrição", "Valor", "%"],
    ["A.Preço de Venda:", PV, "100"],
    ["B.Custo de Aquisição:", CP, int(PCA)],
    ["C.Receita Bruta(A-B):", RB, int(PRB)],
    ["D.Custo Fixo/Administrativo:", CF, int(PCF)],
    ["E.Comissão de vendas:", VCV, int(CV)],
    ["F.Impostos:", VI, int(IV)],
    ["G.Outros Custos(D+E+F):", OC, int(POC)],
    ["H.Rentabilidade(C-G):", R, int(ML)]
]

print(tabulate(tabela, headers="firstrow", tablefmt="rounded_outline", floatfmt=".2f"))

#Classificação de lucro:
if ML>20:
    print("Lucro alto")
elif ML>10 and ML<=20:
    print("Lucro médio")
elif ML>0 and ML<=10:
    print("Lucro baixo")
elif ML==0:
    print("Equilibrio")
elif ML<0:
    print("Prejuízo")
######################################