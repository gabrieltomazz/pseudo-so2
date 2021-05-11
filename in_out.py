import file_manager


def build(rolls):

    listRools = read_cilindro_from_file(rolls)
    fcfs(listRools)
    sstf(listRools)
    scan(listRools)

def read_cilindro_from_file(rools):

    listRools = []
    for rool in rools:
        dados = rool
        listRools.append(dados)

    return listRools


def fcfs(listrools):
    return listrools


def sstf(listrools):
    return listrools


def scan(listrools):
    return listrools

