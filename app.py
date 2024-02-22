import csv
import math
import random
import sys
from time import time

# define quantos testes de cada tipo realizar caso seja um valor maior
# que um, omitir logs de erros e realizar um resumo de precisão e tempo de
# execução médio de cada teste
NUMERO_TESTES = int(sys.argv[1]) if len(sys.argv) > 1 else 100

# esteja certo que o caminho para esse arquivo existe
IRIS_FILE = "Iris.csv"


# nome das classes (espécies)
C_SETOS = "Iris-setosa"
C_VIRG = "Iris-virginica"
C_VERS = "Iris-versicolor"

flores = []
testes = []
treino = []
treino_dmc = []

# metodos para serem testados
metodos = {
    # indica os conjuntos de teste e treino, o k e os valores padrão de
    # taxa de acerto e tempo
    "NN": [(testes, treino, 1), 0.0, 0.0],
    "DMC": [(testes, treino_dmc, 1), 0.0, 0.0],
}

for i in range(3, 15, 2):
    exec(f"metodos['KNN-{i}'] = [(testes, treino, {i}), 0.0, 0.0]")


def log(logs=True, texto="", *args):
    if logs:
        print(texto % args)


# retorna a lista de flores da Iris dataset no diretório atual
def get_list():
    tlist = []
    try:
        file = open(IRIS_FILE)
        reader = csv.reader(file)
        head = next(reader)
        id_pos = 1 if len(head) > 5 else 0

        # pula a primeira linha apenas se ela for cabeçalho
        header_list = (
            [head] + list(reader)
            if head[0].replace(".", "").isdigit()
            else list(reader)
        )
        for el in header_list:
            if len(el) > 4:
                tlist.append([float(e) for e in el[id_pos:-1]] + el[-1:])
    except:
        print("Nenhum arquivo '%s' encontrado! Faça o upload :)" % (IRIS_FILE))
        return

    return tlist


# retorna a distancia euclidiana das medidas de duas flores
def distance(*medidas):  # duas listas: cada uma com as 4 medidas das flores
    # caso ocorra de uma lista ter mais medidas que a outra (inconsistencia)
    # comparar o máximo que der
    m = min(map(len, medidas))
    l = [medidas[0][i] - medidas[1][i] for i in range(m)]
    return math.hypot(*l)


# recebe uma lista de flores e separa por classe
def classificar(flores):
    setosa = []
    virginica = []
    versicolor = []
    for flor in flores:
        if flor[-1] == C_SETOS:
            setosa.append(flor)
        elif flor[-1] == C_VIRG:
            virginica.append(flor)
        if flor[-1] == C_VERS:
            versicolor.append(flor)

    # não necessariamente precisa ser uma lista completa pois apenas o
    # ultimo atributo é consultado
    return (setosa, virginica, versicolor)


# definição dos algoritmos de vizinho mais próximo


# metodo NN puro, retora a flor vizinha da forma mais rapida possivel
def nn(
    flor, conjunto, k=1
):  # variavel k apenas para manter interface igual a função knn
    menorDistancia = None
    florVizinha = None

    for f in conjunto:
        dt = distance(flor[:-1], f[:-1])

        if menorDistancia == None or dt < menorDistancia:
            menorDistancia = dt
            florVizinha = f

    return florVizinha


# metodo NN e KNN: se comporta como NN se k=1 e KNN com k > 1
def knn(flor, conjunto, k=1):
    flores_vizinhas = []

    for i, f in enumerate(conjunto):
        flores_vizinhas.append([i] + [distance(flor[:-1], f[:-1])] + [f[-1]])

    flores_vizinhas.sort(key=lambda v: v[1])  # ordena da menor para a maior

    knvizinhas = classificar(flores_vizinhas[:k])  # classifica as K mais próximas
    flor_vizinha = max(*knvizinhas, key=len)[
        0
    ]  # pega a primeira flor cuja classe aparece mais vezes

    return conjunto[flor_vizinha[0]]


# definição dos algoritmos de DMC


# retorna a centroide de uma lista de flores de mesma classe
def get_centroide(flores_classe):
    med_centroide = [0, 0, 0, 0]
    ln = len(flores_classe)
    for f in flores_classe:
        m = f[:-1]
        for i, value in enumerate(m):
            med_centroide[i] += (
                value / ln
            )  # somar dividindo é o mesmo que somar e depois dividir

    return med_centroide + flores_classe[-1]


# retorna as 3 centroides, uma de cada classe
def dmc(flores):
    classes = classificar(flores)
    centroides = []
    for classe in classes:
        centroides.append(get_centroide(classe))

    return centroides


# definição das funções de testagem


# função geral para a testagem tanto para NN, KNN e DMC
def testagem(nome, testes, treino, k=1, logs=True):
    log(logs, "Teste %s------------------------------\n", nome)

    acertos = 0
    alg = nn if k <= 1 else knn
    for flor in testes:
        res = alg(flor, treino, k)
        if res[-1] != flor[-1]:
            if res == None:
                log(logs, "erro: não foi possivel obter resultado da flor {}", flor)
            else:
                log(
                    logs,
                    "erro: a flor %s teve como resultado a classe %s",
                    flor,
                    res[-1],
                )

            continue

        acertos += 1

    ln = len(testes)
    taxa_acertos = acertos / ln
    log(
        logs,
        "quantidade de erros %d\ntaxa de acertos: %.2f",
        ln - acertos,
        taxa_acertos,
    )
    log(logs, "\n------------------------------")

    return taxa_acertos


def selecionar():
    global testes, treino, treino_dmc

    random.shuffle(flores)
    testes.clear()
    treino.clear()
    treino_dmc.clear()
    testes += flores[:45]
    treino += flores[45:]
    treino_dmc += dmc(treino)


def clock_func(func, *args) -> tuple[float, float]:
    t1 = time()
    res = func(*args)
    return (res, time() - t1)


# função que mede e resume os tempos de execução de cada algoritmo
def medir_desempenho(n):
    log(True, "Iniciando %d testes de cada tipo...", n)

    for i in range(n):
        selecionar()
        for met in metodos:
            res = clock_func(testagem, met, *metodos[met][0], False)
            metodos[met][1] += res[0]
            metodos[met][2] += res[1]

    # ordena os resultados dos testes baseado na taxa de acerto
    perf_list = sorted(metodos.keys(), key=lambda v: metodos[v][1]).__reversed__()
    for met in perf_list:
        log(True, "\nTestes %s\n------------------------------\n", met)
        log(True, "taxa de acertos média: %.4f", metodos[met][1] / n)
        log(True, "tempo de execução médio: %.3f ms", metodos[met][2] * 1000 / n)
        log(True, "\n------------------------------")


def main():
    global flores
    flores = get_list()
    if flores == None:
        return

    if NUMERO_TESTES > 1:
        medir_desempenho(NUMERO_TESTES)
    else:
        selecionar()
        for met in metodos:
            testagem(*[met, *metodos[met][0], True])


main()
