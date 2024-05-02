from tabulate import tabulate
import oracledb
import getpass

#conexão ao sql
userpwd = getpass.getpass("Enter password: ")
connection = oracledb.connect(user="PEDRO", password=userpwd,
                              host="localhost", port=1521, service_name="XEPDB1")
cursor = connection.cursor()

#seleção dos itens na tabela
lista=[]
cursor.execute("select * from Projeto_Integrador")
while True:
    row = cursor.fetchone()
    if row is None:
        break
    lista.append(row)

#lista: 0=prod1 1=prod2 2=prod3 3=prod4 4=prod5 5=prod6
#(no sql) 0-Cod 1-Nome 2-des 3-CP 4-CF 5-CV 6-IV 7-ML

#organização das variáveis
for i in range(len(lista)):
    CP=lista[i][3]
    CF=lista[i][4]
    CV=lista[i][5]
    IV=lista[i][6]
    ML=lista[i][7]

    #Calculo do preço de venda:
    soma=CF+CV+IV+ML
    if soma>100:
        soma = soma * -1

    PV = CP/(1-((soma)/100))
    #################################

    #Custo de aquisição
    PCA=(CP*100)/PV
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

    #organização e impressão das tabelas
    tabela = [
        ["Descrição", "Valor", "%"],
        ["A.Preço de Venda:", PV, "100%"],
        ["B.Custo de Aquisição:", CP, f"{round(PCA)}%"],
        ["C.Receita Bruta(A-B):", RB, f"{round(PRB)}%"],
        ["D.Custo Fixo/Administrativo:", VCF, f"{round(CF)}%"],
        ["E.Comissão de vendas:", VCV, f"{round(CV)}%"],
        ["F.Impostos:", VI, f"{round(IV)}%"],
        ["G.Outros Custos(D+E+F):", OC, f"{round(POC)}%"],
        ["H.Rentabilidade(C-G):", R, f"{round(ML)}%"]
    ]
    cabeçalho=[[lista[i][0], lista[i][1], lista[i][2]]]
    print(tabulate(cabeçalho, tablefmt="rounded_outline"))
    print(tabulate(tabela, headers="firstrow", tablefmt="rounded_outline", floatfmt=".2f"))

    #Classificação de lucro:
    if ML>20:
        print(tabulate([["Lucro alto"]], tablefmt="rounded_outline"))
        print()
    elif ML>10 and ML<=20:
        print(tabulate([["Lucro médio"]], tablefmt="rounded_outline"))
        print()
    elif ML>0 and ML<=10:
        print(tabulate([["Lucro baixo"]], tablefmt="rounded_outline"))
        print()
    elif ML==0:
        print(tabulate([["Equilibro"]], tablefmt="rounded_outline"))
        print()
    elif ML<0:
        print(tabulate([["Prejuízo"]], tablefmt="rounded_outline"))
        print()
    ######################################