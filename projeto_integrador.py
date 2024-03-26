cod_prod=int(input("Digite o código do produto: "))
nome_prod=str(input("Digite o nome do produto: "))
descrição=str(input("Descreva o produto: "))
CP=float(input("Digite o custo do produto: "))
CF=float(input("Digite o custo fixo/adiministrativo: "))
CV=float(input("Digite a comissão de venda: "))
IV=float(input("Digite os impostos sobre a venda: "))
ML=float(input("Digite a margem de lucro desejada: "))

PV = CP/(1-((CF+CV+IV+ML)/100))
print(f"{PV:.2f}")

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