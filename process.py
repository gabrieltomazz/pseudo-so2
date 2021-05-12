import file_manager


def build(process):

    listProcess = read_process_from_file(process)

    # retorno = fifo(listProcess)
    # print('FIFO', end='')

    retorno = sjf(listProcess)
    print('SJF', end='')

    # retorno = round_robin(listProcess)
    # print('RR', end='')
    listProcess = retorno[0]
    temp_execucao = retorno[1]

    #ordena por id pra facilitar o print
    listProcess = sorted(listProcess, key=lambda row: row['id'])


    somaTurnarounds = 0.0
    somaTempoRespostas = 0.0
    somaTempoEspera = 0.0
    if len(listProcess) != 0:
        for p in listProcess:
            # calcular TURNAROUND (termino_execucao - temp_chegada)
            somaTurnarounds += p['termino_execucao'] - p['temp_chegada']


            # calcular Tempo de Resposta (tempo de espera / qtd_vezes_pronto => (termino_execucao - temp_chegada) / qtd_vezes_pronto)
            #print('tempoResposta id[' + str(p['id']) + '] = ' + str(p['termino_execucao']) + '-' + str(p['temp_chegada']) +'-'+str(p['temp_exec']) + ' / ' + str(p['qtd_vezes_pronto']))
            #print('tempoResposta id[' + str(p['id']) + '] = ' + str(p['tempo_espera']))
            #somaTempoRespostas += (p['termino_execucao'] - p['temp_chegada'] - p['temp_exec']) / p['qtd_vezes_pronto']
            somaTempoRespostas += (p['termino_execucao'] - p['temp_chegada'] - p['temp_exec']) / p['qtd_vezes_pronto']
            #print('soma tempo respostas = '+ str(somaTempoRespostas))


            # calcular Tempo de Espera (termino_execucao - temp_chegada - temp_exec)
            somaTempoEspera += p['termino_execucao'] - p['temp_chegada'] - p['temp_exec']


        mediaTurnaround = somaTurnarounds / len(listProcess)
        mediaTempoRespostas = somaTempoRespostas / len(listProcess)
        mediaTempoEspera = somaTempoEspera / len(listProcess)
        # for p in listProcess:
        #     print('id ['+str(p['id'])+'] de '+str(p['comeco_execucao'])+' ate '+str(p['termino_execucao']))
        print(' '+str(mediaTurnaround)+' '+str(mediaTempoRespostas)+' ' +str(mediaTempoEspera))


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
        dados['qtd_vezes_pronto'] = 0
        dados['comeco_execucao'] = -1
        dados['termino_execucao'] = 0
        dados['tempo_espera'] = 0
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

        output += "Rodar processo ["+str(proc['id'])+"] de ["+str(tempo_chegada) + "] ate ["+str(temp_execucao + proc['temp_exec'])+"] \n"

        print("Rodar processo ["+str(proc['id'])+"] de ["+str(tempo_chegada) + "] ate ["+str(temp_execucao + proc['temp_exec'])+"]")

        temp_execucao = temp_execucao + proc['temp_exec']
        proc['termino_execucao'] = temp_execucao

    file_manager.write(output, 'process_fifo_result')
    return [sortedProcess, temp_execucao]


# def sjf(listprocess):
#     sortedProcess = sorted(listprocess, key=lambda row: (row['temp_chegada'], row['temp_exec']))
#     temp_execucao = 0
#
#     for proc in sortedProcess:
#         if proc['temp_chegada'] >= temp_execucao:
#             tempo_chegada = proc['temp_chegada']
#         else:
#             tempo_chegada = temp_execucao
#
#         print("Rodar processo [" + str(proc['id']) + "] de [" + str(tempo_chegada) + "] ate [" + str(temp_execucao + proc['temp_exec']) + "]")
#         sortedProcess.remove(proc)
#         sortedProcess = sorted(sortedProcess, key=lambda row: (temp_execucao >= row['temp_chegada'])) #(row['temp_chegada'], row['temp_exec'])
#         print(" length: "+str(len(sortedProcess)))
#         temp_execucao = temp_execucao + proc['temp_exec']
#
#     # while len(sortedProcess) > 0:
#
#
#     # for proc in sortedProcess:
#     #
#     #     if proc['temp_chegada'] < temp_execucao:
#     #         readyProcess.append(proc)
#     #
#     # readyProcess = sorted(readyProcess, key=lambda row: (row['temp_exec']))

def sjf(listEntrada):
    listProcess = listEntrada
    temp_execucao = 0
    listReady = []
    listDone = []
    #enquanto houver processo chegando ou pronto
    while len(listProcess) + len(listReady) > 0:

        #procura por processos que já chegaram
        i = 0
        while i < len(listProcess):
            if listProcess[i]['temp_chegada'] <= temp_execucao:
                print('\033[1;32m\tO processo [' + str(listProcess[i]['id']) + '] entrou para a fila de pronto no tempo ' + str(listProcess[i]['temp_chegada']) + '\033[0m')
                listProcess[i]['qtd_vezes_pronto'] += 1
                listProcess[i]['clock_ultima_execucao'] = temp_execucao
                listReady.append(listProcess[i])
                listProcess.pop(i)
                #decrementa contador pois um elemento saiu da lista
                i -= 1
            #incrementa contador
            i += 1

        #coloca o processo de menor tamanho no começo da lista
        listReady = sorted(listReady, key=lambda row: row['temp_exec'])
        print('id do primeiro: ['+ str(listReady[0]['id']) + ']')

        #verifica se há processos prontos
        if len(listReady) == 0:
            #anda um clock a espera da chegada de novos processos
            temp_execucao += 1
        else:

            #seta os valores de execucao do processo
            listReady[0]['comeco_execucao'] = temp_execucao
            listReady[0]['termino_execucao'] = temp_execucao + listReady[0]['temp_exec']


            #print output
            print('Rodar processo ' + str(listReady[0]['id']) + ' de [' + str(temp_execucao) + '] ate [' + str(listReady[0]['temp_exec'] + temp_execucao) + ']')

            #atualiza tempo execucao
            temp_execucao += listReady[0]['temp_exec']

            #adiciona na lista de concluido e remove da lista de pronto
            listDone.append(listReady.pop(0))

    return [listDone, temp_execucao]

def round_robin(listEntrada):
    listProcess = listEntrada
    quantum = 2
    temp_execucao = 0
    listReady = []
    listDone = []
    #algoritmo da professora adiciona o ultimo executado no final da fila depois dos que ficaram prontos durante o quantum,
    #logo precisa de um buffer pra inserir no final depois de processar os novos processos
    lastProcess = 0
    lastProcessForDebug = 0
    #print(str(len(listProcess)))
    #enquanto houver processo chegando ou pronto
    while (len(listProcess) + len(listReady) > 0) or lastProcess != 0:
        #print('tempo de execucao: ' + str(temp_execucao))
        #procura por processos que já chegaram para o tempo
        i = 0
        while i < len(listProcess):
            #print('iterador i = '+ str(i) + ' id: ' + str(listProcess[i]['id']) + ' tempchegada: ' + str(listProcess[i]['temp_chegada']) + ' <= ' + str(temp_execucao))
            if listProcess[i]['temp_chegada'] <= temp_execucao:
                print('\033[1;32m\tO processo [' + str(listProcess[i]['id']) + '] entrou para a fila de pronto no tempo ' + str(temp_execucao) + '\033[0m')
                listProcess[i]['qtd_vezes_pronto'] += 1
                listProcess[i]['clock_ultima_execucao'] = temp_execucao
                listReady.append(listProcess[i])
                listProcess.pop(i)
                i -= 1
                #print('tamanho da lista listProcess: ' + str(len(listProcess)))
            i += 1
            #print('cheguei final do while,  ' + str(i) + '< ' + str(len(listProcess)) + ' é '+ str(i < len(listProcess)))
        #coloca o ultimo executado no final da lista
        if lastProcess != 0:
            listReady.append(lastProcess)
            lastProcess = 0
        #verifica se há processos prontos
        if len(listReady) == 0:
            #anda um clock a espera da chegada de novos processos
            temp_execucao += 1
        else:
            #executa o processo
            i = 0
            #verifica a cada clock se o processo acaba antes do quantum
            #contador i serve para saber quantos clocks foram usados para o processo
            if listReady[0]['clock_ultima_execucao'] != 0:
                listReady[0]['tempo_espera'] += temp_execucao - listReady[0]['clock_ultima_execucao']
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
                #processo acabou
                print("\033[34m\tterminou o processo [" + str(listReady[0]['id']) + "]\033[0m")
                listReady[0]['termino_execucao'] = temp_execucao
                listDone.append(listReady.pop(0))
            #se nao acabou, joga pro final da lista
            else:
                # #joga pro final da fila e incrementa a qtd de vezes pronto
                # if lastProcessForDebug != 0:
                #     if listReady[0]['id'] != lastProcessForDebug['id']:
                listReady[0]['qtd_vezes_pronto'] += 1
                listReady[0]['clock_ultima_execucao'] = temp_execucao
                #registra o processo como ultimo
                lastProcess = listReady[0]
                lastProcessForDebug = listReady[0]
                #remove do começo
                listReady.pop(0)
    return [listDone, temp_execucao]




