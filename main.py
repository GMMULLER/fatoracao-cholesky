from math import sqrt

#verificar se matriz eh simetrica e positiva definida?
#precisa resolver o sistema?
#a matriz dos coeficientes sera sempre simetrica?
#podemos transformar a matriz dos coeficientes numa matriz diagonal inferior?

# def cholesky(A):
#     G = intanciaMatrizMesmoTamanho(A)

#     for i in range(len(G)):
#         for k in range(i + 1):

#             aux = sum(G[i][j] * G[k][j] for j in range(k))

#             if (i == k): #Elementos diagonais.
#                 G[i][k] = sqrt(A[i][i] - aux)

#             else:
#                 G[i][k] = (1.0 / G[k][k] * (A[i][k] - aux))

#     return G

def cholesky(A):

    lbi = 0 
    for coluna in range(len(A[0])):
        if A[0][coluna] == 0:
            lbi = coluna
        else: 
            break
    lbi += 1

    for i in range(len(A)):
        for k in range(i + 1):
            
            aux = sum(getPosBandMatrix(i,j,A,lbi) * getPosBandMatrix(k,j,A,lbi) for j in range(k))

            if (i == k): #Elementos diagonais.
                setPosBandMatrix(sqrt(getPosBandMatrix(i,i,A,lbi) - aux), i, k, A, lbi)

            else:
                setPosBandMatrix(1.0 / getPosBandMatrix(k,k,A,lbi) * (getPosBandMatrix(i,k,A,lbi) - aux), i, k, A, lbi)

    return A

def transposta(m):
    result = intanciaMatrizMesmoTamanho(m)

    for i in range(len(m)):
        for j in range(len(m[0])):
            result[j][i] = m[i][j]

    return result

def intanciaMatrizMesmoTamanho(m):
    result = []
    for i in range(len(m)):
        aux = []
        for j in range(len(m[0])):
            aux.append(0.0)
        result.append(aux)
    return result

def calculaLargurasBanda(m):

    larguraInferior = 0
    for i in range(1, len(m)):
        if m[i][0] != 0:
            larguraInferior = i

    larguraSuperior = 0
    for j in range(1, len(m[0])):
        if m[0][j] != 0:
            larguraSuperior = j

    return {"larguraInferior": larguraInferior, "larguraSuperior": larguraSuperior}

#Qualquer posicao fora da banda retornara 0
def getPosBandMatrix(i, j, m, lbi):

    if(i >= len(m) or i < 0 or (j-i+lbi) >= len(m[0]) or (j-i+lbi) < 0):
        return 0

    return m[i][j-i+lbi]

def setPosBandMatrix(valor, i, j, m, lbi):

    if not (i >= len(m) or i < 0 or (j-i+lbi) >= len(m[0]) or (j-i+lbi) < 0):
        m[i][j-i+lbi] = valor

def convertePosicao(i, j, lbi):

    return {"i": i, "j": j-i+lbi}

def criaMatrizReduzida(nColunas, lbi, lbs):

    linha = nColunas
    coluna = 1+lbi+lbs

    m = [[0 for i in range(coluna)] for j in range(linha)]

    return m

def printMatriz(m):
    for r in m:
        print(r)
    return

def converteMatriz(m):
    lb = calculaLargurasBanda(m)

    matriz_nova = criaMatrizReduzida(len(m[0]), lb['larguraInferior'], lb['larguraSuperior'])

    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i][j] != 0:
                novas_pos = convertePosicao(i, j, lb['larguraInferior'])
                matriz_nova[novas_pos['i']][novas_pos['j']] = m[i][j]

    return matriz_nova

def main():
    A = [[4, 12, -16], [12, 37, -43], [-16, -43, 98]]
    G = cholesky(A)
    GT = transposta(G)
    print("A:")
    printMatriz(A)

    print("G:")
    printMatriz(G)

    print("GT:")
    printMatriz(GT)
    return

# matriz_teste1= [
#     [0, 0, 4, 1, -1],
#     [0, 1, 4, 1, -1],
#     [-1, 1, 4, 1, -1],
#     [-1, 1, 4, 1, -1],
#     [-1, 1, 4, 1, -1],
#     [-1, 1, 4, 1, -1],
#     [-1, 1, 4, 1, -1],
#     [-1, 1, 4, 1, -1],
#     [-1, 1, 4, 1, 0],
#     [-1, 1, 4, 0, 0]
# ]

# Ax = b
# G . GT . x = b
# G . y = b -> Primeiro acha y
# GT . x = y -> depois acha x
# numero de linhas compacta = numero de colunas grande

teste_resolvido1 = [
    [2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.5, 1.9364916731037085, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [-0.5, 0.6454972243679027, 1.8257418583505538, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, -0.5163977794943222, 0.7302967433402214, 1.7888543819998317, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, -0.5477225575051661, 0.7826237921249264, 1.7571283390805579, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, -0.5590169943749475, 0.8180961902601788, 1.737302110596134, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, -0.5691103932244722, 0.8435994152056344, 1.721758806275896, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, -0.5756051258447284, 0.8628270940952736, 1.7100316209931266, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.580801443474516, 0.8778382828076902, 1.700608606498028, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5847845079140905, 0.889885081409883, 1.6929653337229917]
]

# matriz_teste2 = [
#     [0, 0, 6],
#     [0, 15, 55],
#     [55, 225, 979]
# ]

# teste_resolvido2 = [
#     [2.449489742783178, 0.0, 0.0],
#     [6.123724356957946, 4.183300132670377, 0.0],
#     [22.45365597551247, 20.916500663351886, 6.110100926607781],
# ]

# resolvido2 = cholesky(matriz_teste2)

# for i in range(len(teste_resolvido2)):
#     for j in range(len(teste_resolvido2[0])):
#         print(teste_resolvido2[i][j], getPosBandMatrix(i,j,resolvido2,2))

for i in converteMatriz(teste_resolvido1):
    print(i)
# main()


