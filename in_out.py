import numpy


def build(rolls):

    # le as requisicoes e monta uma lista
    listRequests = read_cilindro_from_file(rolls)

    # chama os funcoes de cada algoritmo
    fcfs(listRequests)
    sstf(listRequests)
    scan(listRequests)

# le as requisicoes e monta uma lista
def read_cilindro_from_file(self):

    newListRools = []
    for rool in self:
        dados = int(rool)
        newListRools.append(dados)

    return newListRools


# fcfs
def fcfs(listrequests):

    # faz uma copia da lista de requisicoes
    listrools_fcfs = list.copy(listrequests)

    # pega o tamanho do cilindro
    head = listrools_fcfs[0]
    listrools_fcfs.remove(head)

    # verifica se existe algum requisicao fora do tamanho do cilindro
    for rool in listrools_fcfs:
        if rool > head:
            print(f"ERROR! Incorrect Position! {rool} ")
            listrools_fcfs.remove(rool)

    # funcao diff do python para pegar diferenca entre posicoes
    result = numpy.diff(listrools_fcfs)
    seeks = 0

    # calculo do seek
    for res in result:
        seeks = seeks + abs(res)
    print("FCFS "+str(seeks))


# sstf
def sstf(listrequests):

    # faz uma copia da lista de requisicoes
    listrools_sstf = list.copy(listrequests)

    # pega o tamanho do cilindro
    head = listrools_sstf[0]
    listrools_sstf.remove(head)

    seek = 0
    min_position = listrools_sstf[0]

    while len(listrools_sstf) > 1:
        listrools_sstf.remove(min_position)
        # funcao retorna a menor seek possivel
        min_seek, min_position = smallest_seek(listrools_sstf, min_position, head)
        # calculo do seek
        seek = seek+min_seek

    print("SSTF "+str(seek))

# scan
def scan(listrequests):
    listrools_scan = list.copy(listrequests)

    # pega da posicao inicial o tamanho do cilindro
    head = listrools_scan[0]
    listrools_scan.remove(head)

    # inicia o seek
    seek = 0

    # pega posicao inicial
    min_position = listrools_scan[0]
    # insere a posicao 0 no cilindro
    listrools_scan.append(0)

    # insere a sentido inicial de deslocamente
    direction = 'left'

    while len(listrools_scan) > 1:
        listrools_scan.remove(min_position)
        #  funcao retorna a menor seek possivel utilizando a direcao de deslocamento
        min_seek, min_position, direction = smallest_seek_direction(listrools_scan, min_position, direction, head)
        seek = seek + min_seek

    print("SCAN " + str(seek))


# menor seek possivel
def smallest_seek(listrools_sstf, position, head):
    min_seek = max(listrools_sstf)
    min_position = 0

    for rool in listrools_sstf:

        # verifica se existe uma posicao fora do cilindro
        if rool > head:
            print(f"ERROR! Incorrect Position! {rool} ")
            listrools_sstf.remove(rool)

        # culculo do menor seek
        seek = abs(position - rool)
        if seek < min_seek:
            min_seek = seek
            min_position = rool

    return min_seek, min_position


# menor seek possivel por direcao
def smallest_seek_direction(listrools_scan, position, direction, head):
    min_seek = max(listrools_scan)
    min_position = 0

    if position == 0:
        direction = 'right'

    for rool in listrools_scan:

        # verifica se existe uma posicao fora do cilindro
        if rool > head:
            print(f"ERROR! Incorrect Position! {rool} ")
            listrools_scan.remove(rool)

        # verifica a posicao de leitura
        if direction == 'left':
            if rool <= position:
                seek = abs(position - rool)
                if seek < min_seek:
                    min_seek = seek
                    min_position = rool
        else:
            if rool > position:
                seek = abs(position - rool)
                if seek < min_seek:
                    min_seek = seek
                    min_position = rool

    return min_seek, min_position, direction



