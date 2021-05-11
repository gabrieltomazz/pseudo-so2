import file_manager

def build(process):

    listProcess = read_process_from_file(process)
    print('Processo')
    for p in listProcess:
        print(str(p['temp_chegada'])+' '+str(p['temp_exec']))


def read_process_from_file(process):

    listProcess = []
    id = 1

    for proc in process:
        dados = {}
        coluna = proc.split(' ')
        dados['id'] = id
        dados['temp_chegada'] = int(coluna[0])
        dados['temp_exec'] = int(coluna[1])
        listProcess = listProcess + [dados]
        id = id +1

    return fifo(listProcess)


def fifo(listprocess):
    sortedProcess = sorted(listprocess, key=lambda row: row['temp_chegada'])
    temp_execucao = 0
    output = ""

    for proc in sortedProcess:
        if proc['temp_chegada'] >= temp_execucao:
            tempo_chegada = proc['temp_chegada']
        else:
            tempo_chegada = temp_execucao
        output += "Rodar processo ["+str(proc['id'])+"] de ["+str(tempo_chegada) + "] ate ["+str(temp_execucao + proc['temp_exec'])+"] \n"
        print("Rodar processo ["+str(proc['id'])+"] de ["+str(tempo_chegada) + "] ate ["+str(temp_execucao + proc['temp_exec'])+"]")
        temp_execucao = temp_execucao + proc['temp_exec']

    file_manager.write(output, 'process_fifo_result')
    return sortedProcess



# "Rodar processo [0] de [0] ate [20]"

# 0: {
#     'temp_chegada'= 1
#     'temp_exec': 20
# },
# 1: {
#     'temp_chegada'= 2
#     'temp_exec': 20
# }
