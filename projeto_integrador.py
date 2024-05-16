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

    #função que classifica o lucro
    def classificaçãolucro(margem):
        if margem>20:
            print(tabulate([["Lucro alto"]], tablefmt="rounded_outline"))
            print("-"*50)
        elif margem>10 and ML<=20:
            print(tabulate([["Lucro médio"]], tablefmt="rounded_outline"))
            print("-"*50)
        elif margem>0 and ML<=10:
            print(tabulate([["Lucro baixo"]], tablefmt="rounded_outline"))
            print("-"*50)
        elif margem==0:
            print(tabulate([["Equilibro"]], tablefmt="rounded_outline"))
            print("-"*50)
        elif margem<0:
            print(tabulate([["Prejuízo"]], tablefmt="rounded_outline"))
            print("-"*50)

    
    #Menu7
    print("-"*50)
    sel1=int(input("Digite: \n 1-Inserir Produto \n 2-Alterar Produto \n 3-Apagar Produto \n 4-Listar Produtos \n 5-Sair \n"))
    print("-"*50)

    if sel1 == 1:
        soma = 101
        while soma>=100:
            #Leitura dos dados:
            cod_prod=int(input("Digite o código do produto: "))
            nome_prod=str(input("Digite o nome do produto: "))
            descricao=str(input("Descreva o produto: "))
            CP=float(input("Digite o custo do produto(R$): "))
            CF=float(input("Digite o custo fixo/adiministrativo(%): "))
            CV=float(input("Digite a comissão de venda(%): "))
            IV=float(input("Digite os impostos sobre a venda(%): "))
            ML=float(input("Digite a margem de lucro desejada(%): "))
            soma=CF+CV+IV+ML
            if soma>100:
                print("Valores não permitidos, tente novamente.")   
        #Calculo do preço de venda:
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
            ["B.Custo de Aquisição:", CP, f"{round(PCA)}%"],
            ["C.Receita Bruta(A-B):", RB, f"{round(PRB)}%"],
            ["D.Custo Fixo/Administrativo:", VCF, f"{round(CF)}%"],
            ["E.Comissão de vendas:", VCV, f"{round(CV)}%"],
            ["F.Impostos:", VI, f"{round(IV)}%"],
            ["G.Outros Custos(D+E+F):", OC, f"{round(POC)}%"],
            ["H.Rentabilidade(C-G):", R, f"{round(ML)}%"]
        ]

        cabeçalho=[[cod_prod, nome_prod, descricao]]
        print(tabulate(cabeçalho, tablefmt="rounded_outline"))
        print(tabulate(tabela, headers="firstrow", tablefmt="rounded_outline", floatfmt=".2f"))

        #Classificação de lucro:
        classificaçãolucro(ML)
        ######################################

        #Inserção dos valores no banco de dados
        dados = [
            (cod_prod, nome_prod, descricao, CP, CF, CV, IV, ML),
        ]

        cursor.executemany("INSERT INTO Projeto_Integrador (COD_PROD, NOME_PROD, DESCRICAO, CP, CF, CV, IV, ML) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)", dados)
        print("Valores inseridos no banco de dados")
        connection.commit()
    
    if sel1 == 2: #alterar produtos
        sel2 = int(input("Digite o código do produto que deseja alterar: "))
        cód=[sel2]
        cursor.execute("select * from Projeto_Integrador WHERE cod_prod = :1 ", cód)
        prod=cursor.fetchall()
        print(f"{prod} \n {"-"*50}")
        p1 = input("Deseja alterar o nome do produto? S/N: ").upper() 
        if p1 == "S":
            novovalor=input("Digite o novo nome: ")
            alt=[(novovalor, sel2)]
            cursor.executemany("""UPDATE Projeto_Integrador set NOME_PROD=:1 WHERE COD_PROD=:2""", alt)
            connection.commit()
            print("-"*50)
        p1 = input("Deseja alterar a descrição do produto? S/N: ").upper()
        if p1 == "S":
            novovalor=input("Digite a nova descrição: ")  
            alt=[(novovalor, sel2)]
            cursor.executemany("""UPDATE Projeto_Integrador set DESCRICAO=:1 WHERE COD_PROD=:2""", alt)
            connection.commit()
            print("-"*50)
        p1 = input("Deseja alterar o custo do produto? S/N: ").upper()
        if p1 == "S":
            novovalor=float(input("Digite o novo custo: "))
            alt=[(novovalor, sel2)]
            cursor.executemany("""UPDATE Projeto_Integrador set CP=:1 WHERE COD_PROD=:2""", alt)
            connection.commit()
            print("-"*50)
        p1 = input("Deseja alterar o custo fixo do produto? S/N: ").upper()
        if p1 == "S":
            novovalor=float(input("Digite o novo custo fixo: "))
            alt=[(novovalor, sel2)]
            cursor.executemany("""UPDATE Projeto_Integrador set CF=:1 WHERE COD_PROD=:2""", alt)
            connection.commit()
            print("-"*50)
        p1 = input("Deseja alterar a comissão de venda do produto? S/N: ").upper()
        if p1 == "S":
            novovalor=float(input("Digite a nova comissão de venda do produto: "))
            alt=[(novovalor, sel2)]
            cursor.executemany("""UPDATE Projeto_Integrador set CV=:1 WHERE COD_PROD=:2""", alt)
            connection.commit()
            print("-"*50)
        p1 = input("Deseja alterar os impostos do produto? S/N: ").upper()
        if p1 == "S":
            novovalor=float(input("Digite o novo imposto do produto: "))
            alt=[(novovalor, sel2)]
            cursor.executemany("""UPDATE Projeto_Integrador set IV=:1 WHERE COD_PROD=:2""", alt)
            connection.commit()
            print("-"*50)
        p1 = input("Deseja alterar a margem de lucro do produto? S/N: ").upper()
        if p1 == "S":
            novovalor=float(input("Digite a nova margem de lucro: "))
            alt=[(novovalor, sel2)]
            cursor.executemany("""UPDATE Projeto_Integrador set ML=:1 WHERE COD_PROD=:2""", alt)
            connection.commit()
            print("-"*50)
        print("Alterações feitas.")

    if sel1 == 3: #apagar dados
        select = input("Digite:\n 1-Apagar todos os produtos\n 2-Apagar produto específico: ")
        print("-"*50)
        if select == '1':
            confirmar=input("Deseja mesmo apagar todos os produtos do banco de dados? S/N: ").upper()
            if confirmar == "S":
                cursor.execute("TRUNCATE TABLE Projeto_Integrador")
                print(f"{'-'*50}\nBanco de dados zerado.")
            else:
                print(f"{'-'*50}\nOperação cancelada.")
        elif select == '2':
            código = input("Digite o código do produto que deseja apagar: ")
            cod=[código]
            cursor.execute("SELECT * FROM Projeto_Integrador WHERE COD_PROD = :1", cod)
            print(cursor.fetchall())
            select=input("Deseja mesmo deletar o produto? S/N: ").upper()
            if select == "S":
                cursor.execute("DELETE FROM Projeto_Integrador WHERE COD_PROD = :1", cod)
                connection.commit()
                print(f"{'-'*50}\nProduto apagado.")
            else:
                print(f"{'-'*50}\nOperação cancelada.")

    if sel1 == 4:  #seleção dos itens na tabela
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
                classificaçãolucro(ML)
                ######################################

    cursor.close
    connection.close()