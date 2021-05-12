import file_manager


def build(processFile):
    listProcess = read_process_from_file(processFile)

    # chama FIFO e imprime
    retornoFIFO = fifo(copy_processList(listProcess))
    print('FIFO', end='')
    calculaEstatisticas(retornoFIFO[0])

    # chama SJF e imprime
    retornoSJF = sjf(copy_processList(listProcess))
    print('SJF', end='')
    calculaEstatisticas(retornoSJF[0])

    # chama Round Robin e imprime
    retornoRR = round_robin(copy_processList(listProcess))
    print('RR', end='')
    calculaEstatisticas(retornoRR[0])

    # ordena por id pra facilitar o print
    listProcess = sorted(listProcess, key=lambda row: row['id'])

def copy_processList(processList):
    newList = []
    for proc in processList:
        newList.append(proc.copy())
    return newList

def read_process_from_file(process):
    listProcess = []
    id = 0

    for proc in process:
        dados = {}
        coluna = proc.split(' ')
        dados['id'] = id
        dados['temp_chegada'] = int(coluna[0])
        coluna1 = int(coluna[1])
        #tempo de execucao necessario
        dados['temp_exec'] = coluna1
        #tempo restante de execucao
        dados['temp_exec_faltando'] = coluna1
        #quantas vezes o processo ficou no estado ready, usado também para inferir quantas vezes ficou em espera
        dados['qtd_vezes_pronto'] = 0
        #armazena o clock em que houve a primeira execucao, -1 indica que nunca foi executado
        dados['comeco_execucao'] = -1
        #armazena o clock em que o processo finalizou sua execucao
        dados['termino_execucao'] = 0
        #armazena o tempo em que o processo ficou pronto mas não executando
        dados['tempo_espera'] = 0
        #armazena o clock da ultima vez que foi escalonado
        dados['clock_ultima_execucao'] = 0
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
        proc['comeco_execucao'] = temp_execucao
        proc['qtd_vezes_pronto'] = 1
        proc['clock_ultima_execucao'] = temp_execucao

        output += "Rodar processo [" + str(proc['id']) + "] de [" + str(tempo_chegada) + "] ate [" + str(
            temp_execucao + proc['temp_exec']) + "] \n"

        temp_execucao = temp_execucao + proc['temp_exec']
        proc['termino_execucao'] = temp_execucao

    file_manager.write(output, 'process_fifo_result')
    return [sortedProcess, temp_execucao]


def sjf(listEntrada):
    output = ""
    # lista de todos os processos do arquivo txt
    listProcess = listEntrada
    # tempo de execucao, basicamente o clock do processador
    temp_execucao = 0
    # lista de prontos, armazena todos os procesos aptos a serem executados
    listReady = []
    # lista de finalizado possui os processos com suas estatísticas já calculadas
    listDone = []
    # enquanto houver processo chegando ou pronto
    while len(listProcess) + len(listReady) > 0:

        # procura por processos que já chegaram
        i = 0
        while i < len(listProcess):
            if listProcess[i]['temp_chegada'] <= temp_execucao:
                # print('\033[1;32m\tO processo [' + str(
                #     listProcess[i]['id']) + '] entrou para a fila de pronto no tempo ' + str(
                #     listProcess[i]['temp_chegada']) + '\033[0m')
                listProcess[i]['qtd_vezes_pronto'] = 1
                listProcess[i]['clock_ultima_execucao'] = temp_execucao
                listReady.append(listProcess[i])
                listProcess.pop(i)
                # decrementa contador pois um elemento saiu da lista
                i -= 1
            # incrementa contador
            i += 1

        # coloca o processo de menor tamanho no começo da lista
        listReady = sorted(listReady, key=lambda row: row['temp_exec'])
        # print('id do primeiro: [' + str(listReady[0]['id']) + ']')

        # verifica se há processos prontos
        if len(listReady) == 0:
            # anda um clock a espera da chegada de novos processos
            temp_execucao += 1
        else:

            # seta os valores de execucao do processo
            listReady[0]['comeco_execucao'] = temp_execucao
            listReady[0]['termino_execucao'] = temp_execucao + listReady[0]['temp_exec']

            # print output
            output += 'Rodar processo ' + str(listReady[0]['id']) + ' de [' + str(temp_execucao) + '] ate [' + str(
                listReady[0]['temp_exec'] + temp_execucao) + ']\n'

            # atualiza tempo execucao
            temp_execucao += listReady[0]['temp_exec']

            # adiciona na lista de concluido e remove da lista de pronto
            listDone.append(listReady.pop(0))

    file_manager.write(output, 'process_sjf_result')
    return [listDone, temp_execucao]


def round_robin(listEntrada):
    output = ""
    #lista de todos os processos do arquivo txt
    listProcess = listEntrada
    #define o quantum
    quantum = 2
    #tempo de execucao, basicamente o clock do processador
    temp_execucao = 0
    #lista de prontos, armazena todos os procesos aptos a serem executados
    listReady = []
    #lista de finalizado possui os processos com suas estatísticas já calculadas
    listDone = []
    # algoritmo da professora adiciona o ultimo executado no final da fila, depois até dos que ainda estão chegando
    # logo precisa de um buffer temporário com o ultimo executado pra inserir no final depois de
    # inserir os processos que estão chegando
    lastProcess = 0
    # enquanto houver processo chegando ou pronto
    while (len(listProcess) + len(listReady) > 0) or lastProcess != 0:
        # procura por processos que já chegaram para o tempo
        i = 0
        while i < len(listProcess):
            if listProcess[i]['temp_chegada'] <= temp_execucao:
                # print('\033[1;32m\tO processo [' + str(
                #     listProcess[i]['id']) + '] entrou para a fila de pronto no tempo ' + str(temp_execucao) + '\033[0m')
                listProcess[i]['qtd_vezes_pronto'] = 1
                listProcess[i]['clock_ultima_execucao'] = temp_execucao
                listReady.append(listProcess[i])
                listProcess.pop(i)
                i -= 1
                # print('tamanho da lista listProcess: ' + str(len(listProcess)))
            i += 1
        # coloca o ultimo executado no final da lista
        if lastProcess != 0:
            listReady.append(lastProcess)
            lastProcess = 0
        # verifica se há processos prontos
        if len(listReady) == 0:
            # se não tem nenhum pronto, anda um clock a espera da chegada de novos processos
            temp_execucao += 1
        else:
            # como há processos prontos, executa o primeiro da fila até dar o quantum
            i = 0
            # verifica a cada clock se o processo acaba antes do quantum
            # contador i serve para saber quantos clocks foram usados para o processo
            if listReady[0]['clock_ultima_execucao'] != 0:
                listReady[0]['tempo_espera'] += temp_execucao - listReady[0]['clock_ultima_execucao']
            while i < quantum:
                # verifica se é a primeira vez que está executando
                if listReady[0]['comeco_execucao'] == -1:
                    listReady[0]['comeco_execucao'] = temp_execucao
                i += 1
                # print('\ttemp exec ' + str(listReady[0]['temp_exec']) + ' do processo ' + str(listReady[0]['id']))
                listReady[0]['temp_exec_faltando'] -= 1
                if listReady[0]['temp_exec_faltando'] == 0:
                    break
            output += 'Rodar processo ' + str(listReady[0]['id']) + ' de [' + str(temp_execucao) + '] ate [' + str(
                temp_execucao + i) + ']\n'
            # adiciona o tempo de execucao feito pelo processo
            temp_execucao += i
            # verifica se o processo acabou:
            if listReady[0]['temp_exec_faltando'] == 0:
                listReady[0]['termino_execucao'] = temp_execucao
                #se acabou, adiciona na lista de finalizado e remove da lista de pronto
                listDone.append(listReady.pop(0))

            # se nao acabou, joga pro buffer pra ser adicionado no final da lista
            else:
                # #joga pro final da fila e incrementa a qtd de vezes pronto
                listReady[0]['qtd_vezes_pronto'] += 1
                listReady[0]['clock_ultima_execucao'] = temp_execucao
                # registra no buffer de ultimo processo
                lastProcess = listReady[0]
                # remove do começo da lista
                listReady.pop(0)
    file_manager.write(output, 'process_rr_result')
    return [listDone, temp_execucao]


#realiza os cálculos das estatísticas pedidas
def calculaEstatisticas(listProcess):
    somaTurnarounds = 0
    somaTempoRespostas = 0
    somaTempoEspera = 0
    #calcula para cada processo e adiciona na soma
    if len(listProcess) != 0:
        for p in listProcess:
            # calcular TURNAROUND (termino_execucao - temp_chegada)
            somaTurnarounds += p['termino_execucao'] - p['temp_chegada']

            # calcular media Tempo de Resposta de um processo (Tempo de Espera/quantidade de vezes interrompido)
            somaTempoRespostas += (p['termino_execucao'] - p['temp_chegada'] - p['temp_exec']) / p['qtd_vezes_pronto']

            # calcular Tempo de Espera (termino_execucao - temp_chegada - temp_exec)
            somaTempoEspera += p['termino_execucao'] - p['temp_chegada'] - p['temp_exec']

        #calcula a media dos turnaronds
        mediaTurnaround = somaTurnarounds / len(listProcess)
        #calcula a media de tempo de resposta de todos os processos
        mediaTempoRespostas = somaTempoRespostas / len(listProcess)
        #calcula a media do tempo de espera
        mediaTempoEspera = somaTempoEspera / len(listProcess)
        #imprime os valores
        print(' ' + str(round(mediaTurnaround, 2)) + ' ' + str(round(mediaTempoRespostas, 2)) + ' ' + str(round(mediaTempoEspera, 2)))
