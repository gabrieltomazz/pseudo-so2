import file_manager


def build(process):

    listProcess = read_process_from_file(process)
    #fifo(listProcess)
    sjf(listProcess)


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
        id += 1

    return listProcess


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


def sjf(listprocess):
    sortedProcess = sorted(listprocess, key=lambda row: (row['temp_chegada'], row['temp_exec']))
    temp_execucao = 0
    output = ""

    for proc in sortedProcess:
        if proc['temp_chegada'] >= temp_execucao:
            tempo_chegada = proc['temp_chegada']
        else:
            tempo_chegada = temp_execucao

        print("Rodar processo [" + str(proc['id']) + "] de [" + str(tempo_chegada) + "] ate [" + str(temp_execucao + proc['temp_exec']) + "]")
        sortedProcess.remove(proc)
        sortedProcess = sorted(sortedProcess, key=lambda row: (temp_execucao >= row['temp_chegada'])) #(row['temp_chegada'], row['temp_exec'])
        print(" length: "+str(len(sortedProcess)))
        temp_execucao = temp_execucao + proc['temp_exec']

    # while len(sortedProcess) > 0:


    # for proc in sortedProcess:
    #
    #     if proc['temp_chegada'] < temp_execucao:
    #         readyProcess.append(proc)
    #
    # readyProcess = sorted(readyProcess, key=lambda row: (row['temp_exec']))
