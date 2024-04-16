from tabulate import tabulate
import oracledb
import getpass

userpwd = getpass.getpass("Enter password: ")
connection = oracledb.connect(user="PEDROMALINCONICO", password=userpwd,
                              host="localhost", port=1521, service_name="XEPDB1")
cursor = connection.cursor()


#Leitura dos dados:
cod_prod=int(input("Digite o código do produto: "))
nome_prod=str(input("Digite o nome do produto: "))
descricao=str(input("Descreva o produto: "))
CP=float(input("Digite o custo do produto: "))
CF=float(input("Digite o custo fixo/adiministrativo: "))
CV=float(input("Digite a comissão de venda: "))
IV=float(input("Digite os impostos sobre a venda: "))
ML=float(input("Digite a margem de lucro desejada: "))

#Calculo do preço de venda:
soma=CF+CV+IV+ML
if soma>100:
    soma = soma * -1

PV = CP/(1-((soma)/100))
#################################


#Custo de aquisição:
PCA=(CP*100)//PV
#Receita bruta:
RB=PV-CP
PRB=100-PCA
#ValorImposto
VI=(IV/100)*PV
#Comissão
VCV=(CV/100)*PV
#Rentabilidade
R=(ML/100)*PV
#Custofixo:
VCF=(CF/100)*PV
#OutrosCustos
OC=VCF+VCV+VI
POC=CF+CV+IV

tabela = [
    ["Descrição", "Valor", "%"],
    ["A.Preço de Venda:", PV, "100%"],
    ["B.Custo de Aquisição:", CP, f"{PCA}%"],
    ["C.Receita Bruta(A-B):", RB, f"{PRB}%"],
    ["D.Custo Fixo/Administrativo:", VCF, f"{CF}%"],
    ["E.Comissão de vendas:", VCV, f"{CV}%"],
    ["F.Impostos:", VI, f"{IV}%"],
    ["G.Outros Custos(D+E+F):", OC, f"{POC}%"],
    ["H.Rentabilidade(C-G):", R, f"{ML}%"]
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

cursor.execute("insert into Projeto_Integrador values (:1, :2, :3, :4, :5, :6, :7, :8)",
               (1, cod_prod)
               (2, nome_prod)
               (3, descricao)
               (4, CP)
               (5, CF)
               (6, CV)
               (7, IV)
               (8, ML))
connection.commit()