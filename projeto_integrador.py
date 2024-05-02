from tabulate import tabulate
import oracledb
import getpass

userpwd = getpass.getpass("Enter password: ")
sel1=0
while sel1 != 5:
    
    #conexão ao banco de dados
    
    connection = oracledb.connect(user="PEDROMALINCONICO", password=userpwd,
                                host="localhost", port=1521, service_name="XEPDB1")
    cursor = connection.cursor()


    #Menu7
    sel1=int(input("Digite: \n 1-Inserir Produto \n 2-Alterar Produto \n 3-Apagar Produto \n 4-Listar Produtos \n 5-Sair \n"))


    if sel1 == 1:
        #Leitura dos dados:
        cod_prod=int(input("Digite o código do produto: "))
        nome_prod=str(input("Digite o nome do produto: "))
        descricao=str(input("Descreva o produto: "))
        CP=float(input("Digite o custo do produto(R$): "))
        CF=float(input("Digite o custo fixo/adiministrativo(%): "))
        CV=float(input("Digite a comissão de venda(%): "))
        IV=float(input("Digite os impostos sobre a venda(%): "))
        ML=float(input("Digite a margem de lucro desejada(%): "))

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

        #organização e impressão da tabela
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

        #Inserção dos valores no banco de dados
        dados = [
            (cod_prod, nome_prod, descricao, CP, CF, CV, IV, ML),
        ]

        cursor.executemany("INSERT INTO Projeto_Integrador (COD_PROD, NOME_PROD, DESCRICAO, CP, CF, CV, IV, ML) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)", dados)
        print("Valores inseridos no banco de dados")
        connection.commit()
    
    #alterar produtos
    if sel1 == 2:
        codsql=""
        sel2 = int(input("Digite o código do produto que deseja alterar: "))
        cód=[sel2]
        cursor.execute("select * from Projeto_Integrador WHERE cod_prod = :1 ", cód)
        prod=cursor.fetchall()
        print(prod)
        p1 = input("Deseja alterar o nome do produto? S/N: ").upper()
        if p1 == 'S':
            nome=input("Digite o novo nome: ")
            strnome="NOME_PROD="
            codsql=strnome+"'"+nome+"'"
            p1 = input("Deseja alterar a descrição S/N: ").upper()
        else:
            p1 = input("Deseja alterar a descrição S/N: ").upper()
        if p1 == 'S':
            desc=input("Digite a nova descrição: ")
            strdesc="DESCRICAO="
            codsql+=","+strdesc+"'"+desc+"'"
        where="WHERE COD_PROD="
        cod=str(sel2)
        update="UPDATE Projeto_Integrador set "
        codsql='"""'+update+codsql+' '+where+cod+'"""'
        codsql.encode('unicode-escape')
        cursor.execute(codsql)
        connection.commit()
    if sel1 == 4:
        #seleção dos itens na tabela
        lista=[]
        cursor.execute("select * from Projeto_Integrador")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            lista.append(row)
 #(no sql) 0-Cod 1-Nome 2-des 3-CP 4-CF 5-CV 6-IV 7-ML
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

    if sel1 == 3:
        #apagar dados
        select = input("Digite:\n 1-Apagar todos os produtos\n 2-Apagar produto específico: ")
        if select == '1':
            cursor.execute("TRUNCATE TABLE Projeto_Integrador")
        elif select == '2':
            código = input("Digite o código do produto que deseja apagar: ")
            deletar = "DELETE FROM Projeto_Integrador WHERE COD_PROD = :código"
            cursor.execute(deletar, código=código)
            connection.commit()




    cursor.close
    connection.close()