import file_manager


def build(process):

    listProcess = read_process_from_file(process)
    #fifo(listProcess)
    #sjf(listProcess)
    retorno = round_robin(listProcess)
    listProcess = retorno[0]
    temp_execucao = retorno[1]

    listProcess = sorted(listProcess, key=lambda row: row['id'])
    for p in listProcess:
        print('id ['+str(p['id'])+'] de '+str(p['comeco_execucao'])+' ate '+str(p['termino_execucao']))


def read_process_from_file(process):

    listProcess = []
    id = 0

    for proc in process:
        dados = {}
        coluna = proc.split(' ')
        dados['id'] = id
        dados['temp_chegada'] = int(coluna[0])
        dados['temp_exec'] = int(coluna[1])
        dados['temp_exec_faltando'] = dados['temp_exec']
        dados['comeco_execucao'] = -1
        dados['termino_execucao'] = 0
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


def round_robin(listEntrada):
    listProcess = listEntrada
    quantum = 2
    temp_execucao = 0
    listReady = []
    listDone = []
    #print(str(len(listProcess)))
    #enquanto houver processo chegando ou pronto
    while len(listProcess) + len(listReady) > 0:
        #print('tempo de execucao: ' + str(temp_execucao))
        #procura por processos que já chegaram para o tempo
        i = 0
        while i < len(listProcess):
            #print('iterador i = '+ str(i) + ' id: ' + str(listProcess[i]['id']) + ' tempchegada: ' + str(listProcess[i]['temp_chegada']) + ' <= ' + str(temp_execucao))
            if listProcess[i]['temp_chegada'] <= temp_execucao:
                print('\033[1;32m\tO processo [' + str(listProcess[i]['id']) + '] entrou para a fila de pronto no tempo ' + str(temp_execucao) + '\033[0m')
                listReady.append(listProcess[i])
                listProcess.pop(i)
                i -= 1
                #print('tamanho da lista listProcess: ' + str(len(listProcess)))
            i += 1
            #print('cheguei final do while,  ' + str(i) + '< ' + str(len(listProcess)) + ' é '+ str(i < len(listProcess)))

        #verifica se há processos prontos
        if len(listReady) == 0:
            #anda um clock a espera da chegada de novos processos
            temp_execucao += 1
        else:
            #executa o processo
            i = 0
            #verifica a cada clock se o processo acaba antes do quantum
            #contador i serve para saber quantos clocks foram usados para o processo
            while i < quantum:
                #verifica se é a primeira vez que está executando
                if listReady[0]['comeco_execucao'] == -1:
                    listReady[0]['comeco_execucao'] = temp_execucao
                i += 1
                #print('\ttemp exec ' + str(listReady[0]['temp_exec']) + ' do processo ' + str(listReady[0]['id']))
                listReady[0]['temp_exec_faltando'] -= 1
                if listReady[0]['temp_exec_faltando'] == 0:
                    break
            print('Rodar processo ' + str(listReady[0]['id']) + ' de [' + str(temp_execucao) + '] ate [' + str(temp_execucao + i) + ']')
            #adiciona o tempo de execucao feito pelo processo
            temp_execucao += i
            #verifica se o processo acabou:
            if listReady[0]['temp_exec_faltando'] == 0:
                #TODO: executa o que precisa pra registrar o tempo de termino
                print("\033[34m\tterminou o processo [" + str(listReady[0]['id']) + "]\033[0m")
                listReady[0]['termino_execucao'] = temp_execucao
                listDone.append(listReady.pop(0))
            else:
                #joga pro final da fila
                listReady.append(listReady[0])
                #remove do começo
                listReady.pop(0)
    return [listDone, temp_execucao]




