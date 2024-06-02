from tabulate import tabulate
import oracledb
import getpass

userpwd = getpass.getpass("Digite a senha: ")
while userpwd != '123456':
    userpwd = getpass.getpass("Senha errada, digite novamente: ")

sel1=0
#função que classifica o lucro
def classificaçãolucro(margem):
        if margem>20:
            print(tabulate([["Lucro alto"]], tablefmt="rounded_outline"))
            linha()
        elif margem>10: 
            print(tabulate([["Lucro médio"]], tablefmt="rounded_outline"))
            linha()
        elif margem>0: 
            print(tabulate([["Lucro baixo"]], tablefmt="rounded_outline"))
            linha()
        elif margem==0:
            print(tabulate([["Equilibro"]], tablefmt="rounded_outline"))
            linha()
        else:
            print(tabulate([["Prejuízo"]], tablefmt="rounded_outline"))
            linha()

def criptografia(descrição):
    descricao_criptografada=""

    alfabeto = {
        "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10,
        "K": 11, "L": 12, "M": 13, "N": 14, "O": 15, "P": 16, "Q": 17, "R": 18, "S": 19,
        "T": 20, "U": 21, "V": 22, "W": 23, "X": 24, "Y": 25, " ":0, "Z": 26
    }
    #matriz codificadora
    A=([4, 3],
       [1, 2])
    l1=[]
    l2=[]
    cont=0 #variavel cont aumenta de 1 em 1 é usada no if para alternar as produtos em que se insere o valor das letras
    for i in range(len(descrição)):
        cont+=1
        letra=descrição[i]
        chave=letra
        x=alfabeto[chave]
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
                descricao_criptografada += key
    return(descricao_criptografada)

def decifragem(descrição_criptografada):
    descricao_descriptografada=""
    alfabeto = {
        "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10,
        "K": 11, "L": 12, "M": 13, "N": 14, "O": 15, "P": 16, "Q": 17, "R": 18, "S": 19,
        "T": 20, "U": 21, "V": 22, "W": 23, "X": 24, "Y": 25, "Z": 26, " ": 0
    }
    #matriz codificadora inversa
    Ainv=([22, -33],
          [-11, 44])
    l1=[]
    l2=[]
    cont=0
    for i in range(len(descrição_criptografada)):
        cont+=1
        letra=descrição_criptografada[i]
        chave=letra
        x=alfabeto[chave]
        if cont%2!=0:
            l1.append(x)
        else:
            l2.append(x)
    if len(l2)<len(l1):
        ultimoelemento=l1[len(l1)-1]
        l2.append(ultimoelemento)
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
    #pmodulo(P,27)
    p1=[]
    p2=[]
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
    #organização das silabas
    silabas=[]
    for i in range(len(p1)):
        silabas.append(p1[i])
        silabas.append(p2[i])

    #busca das letras no dicionário
    for i in range(len(silabas)):
        valor = silabas[i]
        for key, value in alfabeto.items():
            if value == valor:
                descricao_descriptografada += key
    return(descricao_descriptografada)

def produto_especifico(código):
    produto=[]
    cursor.execute('SELECT * FROM Projeto_Integrador WHERE COD_PROD=:1', código)
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        produto.append(row)
        #(no sql) 0-Cod 1-Nome 2-des 3-CP 4-CF 5-CV 6-IV 7-ML
    COD=produto[0][0]
    NOME=produto[0][1]
    DES=produto[0][2]
    CP=produto[0][3]
    CF=produto[0][4]
    CV=produto[0][5]
    IV=produto[0][6]
    ML=produto[0][7]
    
    #Calculo do preço de venda:
    soma=CF+CV+IV+ML
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
    cabeçalho=[[COD, NOME, decifragem(DES)]]
    print(tabulate(cabeçalho, tablefmt="rounded_outline"))
    print(tabulate(tabela, headers="firstrow", tablefmt="rounded_outline", floatfmt=".2f"))
                
    #Classificação de lucro:
    classificaçãolucro(ML)
    ######################################

def linha():
    print("="*100)

while sel1 != 5:
    
    #conexão ao banco de dados
    
    connection = oracledb.connect(user="PEDROMALINCONICO", password=userpwd,
                                host="localhost", port=1521, service_name="XEPDB1")
    cursor = connection.cursor()

    def checarcodigo(codprod): #função que checa se um codigo está no banco de dados, e se estiver, retorna valor True
        cursor.execute("SELECT COD_PROD FROM Projeto_Integrador")
        codigos=cursor.fetchall()
        for i in range(len(codigos)):
            if codprod in codigos[i]:
                return(True)
    
    def checarseestavazio(): #função que checa se o banco de dados está vazio
        cursor.execute("SELECT * FROM Projeto_Integrador")
        x=cursor.fetchall()
        return(len(x))
    #Menu7
    print(f"|{'='*100}|")
    print("\t\t\t\t | Sistema de Cadastro de Produtos |\n")
    print(f"|{'='*100}|")
    print(f"\t 1-Inserir Produto | 2-Alterar Produto | 3-Apagar Produto | 4-Listar Produtos | 5-Sair ")
    print(f"|{'='*100}|")
    sel1=int(input("| Selecionar:"))
    while sel1<=0 or sel1>5:
        sel1=int(input("| Opção invalida, selecione 1-5:"))
    linha()

    if sel1 == 1: #inserir produtos
        soma = 101
        
        while soma>=100:
            #Leitura dos dados:
            linha()
            cod_prod=int(input("|Digite o código do produto: "))
            while checarcodigo(cod_prod):
                cod_prod=int(input("|Código ja existente no banco de dados, digite outro: "))
                checarcodigo(cod_prod)
            linha()
            nome_prod=str(input("|Digite o nome do produto: "))
            linha()
            descricao=str(input("|Descreva o produto(apenas letras): ")).upper()
            linha()
            CP=float(input("|Digite o custo do produto(R$): "))
            linha()
            CF=float(input("|Digite o custo fixo/adiministrativo(%): "))
            linha()
            CV=float(input("|Digite a comissão de venda(%): "))
            linha()
            IV=float(input("|Digite os impostos sobre a venda(%): "))
            linha()
            ML=float(input("|Digite a margem de lucro desejada(%): "))
            soma=CF+CV+IV+ML
            if soma>100:
                print("|Valores não permitidos, tente novamente.")   
        #Calculo do preço de venda:
        PV = CP/(1-((soma)/100))
        #################################


        #Custo de aquisição:
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

        #criptografar descricao
        descricao_cripto=criptografia(descricao)

        #Inserção dos valores no banco de dados
        dados = [
            (cod_prod, nome_prod, descricao_cripto, CP, CF, CV, IV, ML),
        ]

        cursor.executemany("INSERT INTO Projeto_Integrador (COD_PROD, NOME_PROD, DESCRICAO, CP, CF, CV, IV, ML) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)", dados)
        print("|Valores inseridos no banco de dados")
        connection.commit()
    
    if sel1 == 2: #alterar produtos
        if checarseestavazio() != 0:
            sel2 = int(input("|Digite o código do produto que deseja alterar: "))
            while not checarcodigo(sel2):
                sel2 = int(input("|Produto inexistente, digite outro código: "))
            cód=[sel2]
            produto_especifico(cód)
            p1 = input("|Deseja alterar o código do produto? S/N: ").upper()
            if p1 == "S":
                linha()
                novocod=int(input("Digite o novo código:"))
                while checarcodigo(novocod):
                    novocod=int(input("Código já existen no banco de dados, digite outro:"))

                alt=[(novocod, sel2)]
                cursor.executemany("UPDATE Projeto_Integrador SET COD_PROD=:1 WHERE COD_PROD=:2", alt)
                linha()
                sel2=novocod
                cód=[sel2]
            p1 = input("|Deseja alterar o nome do produto? S/N: ").upper()
            novasoma=101
            linha()
            while novasoma>100:
                print("|Caso o programa peça novamente os valores, a soma de CF, CV, IV e ML é maior do que 100.")
                if p1 == "S":
                    novovalor=input("|Digite o novo nome: ")
                    alt=[(novovalor, sel2)]
                    cursor.executemany("""UPDATE Projeto_Integrador set NOME_PROD=:1 WHERE COD_PROD=:2""", alt)
                    linha()
                else:
                    linha()
                p1 = input("|Deseja alterar a descrição do produto? S/N: ").upper()
                if p1 == "S":
                    novovalor=input("|Digite a nova descrição: ").upper()
                    desc=criptografia(novovalor) 
                    alt=[(desc, sel2)]
                    cursor.executemany("""UPDATE Projeto_Integrador set DESCRICAO=:1 WHERE COD_PROD=:2""", alt)               
                    linha()
                else:
                    linha()
                p1 = input("|Deseja alterar o custo do produto? S/N: ").upper()
                if p1 == "S":
                    novovalor=float(input("|Digite o novo custo: "))
                    alt=[(novovalor, sel2)]
                    cursor.executemany("""UPDATE Projeto_Integrador set CP=:1 WHERE COD_PROD=:2""", alt)
                    linha()
                else:
                    linha()
                p1 = input("|Deseja alterar o custo fixo do produto? S/N: ").upper()
                if p1 == "S":
                    novovalor=float(input("|Digite o novo custo fixo: "))
                    alt=[(novovalor, sel2)]
                    cursor.executemany("""UPDATE Projeto_Integrador set CF=:1 WHERE COD_PROD=:2""", alt)
                    linha()
                else:
                    linha()
                p1 = input("|Deseja alterar a comissão de venda do produto? S/N: ").upper()
                if p1 == "S":
                    novovalor=float(input("|Digite a nova comissão de venda do produto: "))
                    alt=[(novovalor, sel2)]
                    cursor.executemany("""UPDATE Projeto_Integrador set CV=:1 WHERE COD_PROD=:2""", alt)            
                    linha()
                else:
                    linha()
                p1 = input("|Deseja alterar os impostos do produto? S/N: ").upper()
                if p1 == "S":
                    novovalor=float(input("|Digite o novo imposto do produto: "))
                    alt=[(novovalor, sel2)]
                    cursor.executemany("""UPDATE Projeto_Integrador set IV=:1 WHERE COD_PROD=:2""", alt)
                    linha()
                else:
                    linha()
                p1 = input("|Deseja alterar a margem de lucro do produto? S/N: ").upper()
                if p1 == "S":
                    novovalor=float(input("|Digite a nova margem de lucro: "))
                    alt=[(novovalor, sel2)]
                    cursor.executemany("""UPDATE Projeto_Integrador set ML=:1 WHERE COD_PROD=:2""", alt)
                    linha()
                cursor.execute('SELECT CF, CV, IV, ML FROM Projeto_Integrador WHERE COD_PROD=:1 ', cód)
                valores=cursor.fetchall()
                print("CF/CV/IV/ML")
                print(valores)
                novasoma=valores[0][0]+valores[0][1]+valores[0][2]+valores[0][3]

            connection.commit()
            print("Alterações feitas.")
        else:
            print("|Banco de dados vazio.")
            linha()

    if sel1 == 3: #apagar dados
        if checarseestavazio() != 0:
            select = int(input("1-Apagar todos os produtos\n2-Apagar produto específico\n3-Cancelar\nSelecionar: "))
            while select<=0 or select>3:
                select = int(input("Opção invalida, selecione novamente: "))
            linha()
            if select == 1:
                confirmar=input("|Deseja mesmo apagar todos os produtos do banco de dados? S/N: ").upper()
                if confirmar == "S":
                    cursor.execute("TRUNCATE TABLE Projeto_Integrador")
                    print(f"{'='*100}\n|Banco de dados zerado.")
                else:
                    print(f"{'='*100}\n|Operação cancelada.")
            elif select == 2:
                código = int(input("|Digite o código do produto que deseja apagar: "))
                while not checarcodigo(código):
                    código = int(input("|Produto inexistente, digite outro código: "))       
                cod=[código]                 
                produto_especifico(cod)
                select=input("|Deseja mesmo deletar o produto? S/N: ").upper()
                if select == "S":
                    cursor.execute("DELETE FROM Projeto_Integrador WHERE COD_PROD = :1", cod)
                    connection.commit()
                    linha()
                    print("Produto apagado.")
                else:
                    linha()
                    print("Operação cancelada.")
        else:
            print("|Banco de dados vazio.")
            linha()

    if sel1 == 4:  #seleção dos itens na tabela
            if checarseestavazio() != 0:
                produto=[]
                cursor.execute("select * from Projeto_Integrador")
                while True:
                    row = cursor.fetchone()
                    if row is None:
                        break
                    produto.append(row)
                #(no sql) 0-Cod 1-Nome 2-des 3-CP 4-CF 5-CV 6-IV 7-ML
                for i in range(len(produto)):
                    CP=produto[i][3]
                    CF=produto[i][4]
                    CV=produto[i][5]
                    IV=produto[i][6]
                    ML=produto[i][7]

                    #Calculo do preço de venda:
                    soma=CF+CV+IV+ML
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
                    cabeçalho=[[produto[i][0], produto[i][1], decifragem(produto[i][2])]]
                    print(tabulate(cabeçalho, tablefmt="rounded_outline"))
                    print(tabulate(tabela, headers="firstrow", tablefmt="rounded_outline", floatfmt=".2f"))
                    
                    #Classificação de lucro:
                    classificaçãolucro(ML)
                    ######################################
            else:
                print("|Banco de dados vazio.")
                linha()

    cursor.close
    connection.close()