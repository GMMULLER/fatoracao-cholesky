from math import sqrt

# Fatoracao de Cholesky
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

            if (i == k): # Elementos diagonais.
                setPosBandMatrix(sqrt(getPosBandMatrix(i,i,A,lbi) - aux), i, k, A, lbi)

            else:
                setPosBandMatrix(1.0 / getPosBandMatrix(k,k,A,lbi) * (getPosBandMatrix(i,k,A,lbi) - aux), i, k, A, lbi)

    return A

# Dada a matriz G, retorna a posicao i, j da matriz tranposta a G
def getPositionInTranposed(i, j, g, lbi):
    return getPosBandMatrix(j, i, g, lbi)

# Qualquer posicao fora da banda retornara 0
# Acessa a posicao i, j de uma matriz original dada a matriz modificada (armazenada em banda)
def getPosBandMatrix(i, j, m, lbi):

    if(i >= len(m) or i < 0 or (j-i+lbi) >= len(m[0]) or (j-i+lbi) < 0):
        return 0

    return m[i][j-i+lbi]

# Atribui o valor a posicao i, j de uma matriz original dada a matriz modificada (armazenada em banda)
def setPosBandMatrix(valor, i, j, m, lbi):

    if not (i >= len(m) or i < 0 or (j-i+lbi) >= len(m[0]) or (j-i+lbi) < 0):
        m[i][j-i+lbi] = valor

# Cria uma matriz com 0s com os tamanhos passados como parametro
def createMatrix(x, y):
    matrix = []
    for i in range(x):
        matrix.append([0 for j in range(y)])

    return matrix

# Dada a matriz G, obtem a largura de banda inferior da matriz original
def getLbi(g):
    lbi = 0 
    for coluna in range(len(g[0])):
        if g[0][coluna] == 0:
            lbi = coluna
        else: 
            break
    lbi += 1
    return lbi

# Calculo de Y (G * y = b)
def getY(g, b):
    lbi = getLbi(g)

    sizeY = (len(g), len(b[0]))
    y = createMatrix(sizeY[0], sizeY[1])

    for colY in range(sizeY[1]):
        for lineG in range(len(g)):
            for colG in range(lineG - lbi, lineG + 1, 1):
                if colG >= 0:
                    if lineG != colG:
                        y[lineG][colY] -= getPosBandMatrix(lineG, colG, g, lbi) * y[colG][colY]
                    else:
                        y[lineG][colY] += b[lineG][colY]
                        y[lineG][colY] = y[lineG][colY] / getPosBandMatrix(lineG, colG, g, lbi)

    return y

# Calculo de X (GT * x = y)
def getX(g, y):
    lbi = getLbi(g)

    sizeX = (len(g), len(y[0]))
    x = createMatrix(sizeX[0], sizeX[1])

    for colX in range(sizeX[1]):
        for lineG in range(len(g) - 1, -1, -1):
            for colG in range(lineG + lbi, lineG - 1, -1):
                if colG < sizeX[0]:
                    if lineG != colG:
                        x[lineG][colX] -= getPositionInTranposed(lineG, colG, g, lbi) * x[colG][colX]
                    else:
                        x[lineG][colX] += y[lineG][colX]
                        x[lineG][colX] = x[lineG][colX] / getPositionInTranposed(lineG, colG, g, lbi)

    return x

########################## Casos de teste ##########################

# matriz = [
#     [0, 0, 4],
#     [0, 1, 4],
#     [-1, 1, 4],
#     [-1, 1, 4],
#     [-1, 1, 4],
#     [-1, 1, 4],
#     [-1, 1, 4],
#     [-1, 1, 4],
#     [-1, 1, 4],
#     [-1, 1, 4]
# ]
# b = [[4], [5], [4], [4], [4], [4], [4], [4], [5], [4]]
# Gabarito: [[1], [1], [1], [1], [1], [1], [1], [1], [1], [1]]

# matriz = [
#     [0, 0, 6],
#     [0, 15, 55],
#     [55, 225, 979]
# ]
# b = [[76], [295], [1259]]
# Gabarito: [[1], [1], [1]]

# matriz = [
#     [0, 0, 2],
#     [0, -2, 5],
#     [-3, 4, 5]
# ]
# b = [[7], [-12], [-12]]
# Gabarito: [[3], [-2], [1]]

# matriz = [
#     [0, 0, 4],
#     [0, 10, 26],
#     [8, 26, 61]
# ]
# b = [[44], [128], [214]]
# Gabarito: [[-8], [6], [2]]

# Execucao da fatoracao de Cholesky
chole = cholesky(matriz)

# Print do vetor resultante X
print("X:")
for x in getX(chole, getY(chole, b)):
    print(x)