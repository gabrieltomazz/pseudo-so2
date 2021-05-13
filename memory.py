
def build(frames):
    nframes = read_nframes_from_file(frames)
    fifo(nframes)
    second_chance(nframes)
    lru(nframes)


def read_nframes_from_file(frames):

    newListFrames = []
    id = 0
    for frame in frames:
        dados={}
        dados['id'] = id
        dados['ref'] = int(frame)
        newListFrames = newListFrames + [dados]
        id += 1

    return newListFrames


def init_mem(size, type):
    mem = []

    for i in range(size):
        if type == 0:
            mem.append([0, 0])
        else:
            mem.append([0, 0, 0])

    return mem


def fifo(frames):

    # faz uma copia da lista de frames
    listframes_fifo = list.copy(frames)

    # pega tamanho da memoria
    mem_size = listframes_fifo[0]
    listframes_fifo.remove(mem_size)

    # inicializa memoria
    mem_0 = init_mem(mem_size['ref'], 0)
    mem_list = list.copy(mem_0)

    page_fault = 0

    # inicializa a memoria com frames
    for mem in range(len(mem_list)):
        for frame in listframes_fifo:
            if mem_list[mem][1] == 0:
                exist, item = exist_in_page(mem_list, frame['ref'])
                if exist == 0:
                    page_fault += 1
                    mem_list[mem][0] = frame['id']
                    mem_list[mem][1] = frame['ref']
                    listframes_fifo.remove(frame)

    # percorre o restante dos frames
    for frame in listframes_fifo:
            # se o frame não existir soma falta de pagina e insere ele na memoria
            exist, item = exist_in_page(mem_list, frame['ref'])
            if exist == 0:
                page_fault += 1
                first_refer = min(mem_list)
                position = mem_list.index(first_refer)
                mem_list[position][0] = frame['id']
                mem_list[position][1] = frame['ref']
                # listframes_fifo.remove(listframes_fifo[frame])

    print(f"FIFO {page_fault}")


def second_chance(frames):

    # faz uma copia da lista de frames
    listframes_fifo = list.copy(frames)

    # pega tamanho da memoria
    mem_size = listframes_fifo[0]
    listframes_fifo.remove(mem_size)

    # inicializa memoria
    mem_0 = init_mem(mem_size['ref'], 1)
    mem_list = list.copy(mem_0)

    page_fault = 0

    # inicializa a memoria com frames
    for mem in range(len(mem_list)):
        for frame in listframes_fifo:
            if mem_list[mem][1] == 0:
                exist, item = exist_in_page(mem_list, frame['ref'])
                if exist == 1:
                    posix = mem_list.index(item)
                    if mem_list[posix][2] == 3:
                        mem_list[posix][2] = 0
                    else:
                        mem_list[posix][2] += 1
                else:
                    page_fault += 1
                    mem_list[mem][0] = frame['id']
                    mem_list[mem][1] = frame['ref']
                    mem_list[mem][2] = 1
                    listframes_fifo.remove(frame)

    # percorre o restante dos frames
    for frame in listframes_fifo:
        # se o frame não existir soma falta de pagina e insere ele na memoria
        exist, item = exist_in_page(mem_list, frame['ref'])
        if exist == 1:
            posix = mem_list.index(item)
            if mem_list[posix][2] == 3:
                mem_list[posix][2] = 0
            else:
                mem_list[posix][2] += 1
        else:
            page_fault += 1
            first_refer = sorted(mem_list, key=lambda row: (row[0], row[2]))
            first_refer = min(first_refer, key=lambda x: x[2])
            position = mem_list.index(first_refer)
            mem_list[position][0] = frame['id']
            mem_list[position][1] = frame['ref']
            mem_list[position][2] = 1

    print(f"SC {page_fault}")


def lru(frames):

    # faz uma copia da lista de frames
    listframes_fifo = list.copy(frames)

    # pega tamanho da memoria
    mem_size = listframes_fifo[0]
    listframes_fifo.remove(mem_size)

    # inicializa memoria
    mem_0 = init_mem(mem_size['ref'], 1)
    mem_list = list.copy(mem_0)

    page_fault = 0

    # inicializa a memoria com frames

    for mem in range(len(mem_list)):
        if mem_list[mem][1] == 0:
            frame, listframes_fifo = preenche_mem(mem_list, listframes_fifo)
            page_fault += 1
            mem_list[mem][0] = frame['id']
            mem_list[mem][1] = frame['ref']
            mem_list[mem][2] = 1

    # percorre o restante dos frames
    for frame1 in listframes_fifo:
        # se o frame não existir soma falta de pagina e insere ele na memoria
        exist, item = exist_in_page(mem_list, frame1['ref'])
        if exist == 1:
            posix = mem_list.index(item)
            mem_list[posix][2] += 1
        else:
            page_fault += 1
            first_refer = sorted(mem_list, key=lambda row: (row[1]), reverse=True)
            position = mem_list.index(first_refer[0])
            mem_list[position][0] = frame1['id']
            mem_list[position][1] = frame1['ref']
            mem_list[position][2] = 1

    print(f"LRU {page_fault}")


def exist_in_page(mem_list, ref):

    for item in mem_list:
        if ref == item[1]:
            return 1, item

    return 0, 0


def preenche_mem(mem_list, listframes_fifo):

    frame = listframes_fifo[0]
    exist, item = exist_in_page(mem_list, frame['ref'])
    if exist == 1:
        posix = mem_list.index(item)
        mem_list[posix][2] = mem_list[posix][2] + 1
        del listframes_fifo[0]
        preenche_mem(mem_list, listframes_fifo)
        return frame, listframes_fifo
    else:
        del listframes_fifo[0]
        return frame, listframes_fifo


