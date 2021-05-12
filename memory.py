
def build(frames):
    nframes = read_nframes_from_file(frames)
    fifo(nframes)

def read_nframes_from_file(frames):

    newListFrames = []
    id = 0
    for frame in frames:
        dados = {}
        dados['id'] = id
        dados['ref'] = int(frame)
        newListFrames = newListFrames + [dados]
        id += 1

    return newListFrames


def init_mem(size):
    mem = []

    for i in range(size):
        mem.append([0,0])

    # [ [0,0], [0,0], [0,0], [0,0]]

    return mem


def fifo(frames):

    # faz uma copia da lista de frames
    listframes_fifo = list.copy(frames)

    # pega tamanho da memoria
    mem_size = listframes_fifo[0]
    listframes_fifo.remove(mem_size)

    # inicializa memoria
    mem_0 = init_mem(mem_size['ref'])
    mem_list = list.copy(mem_0)

    page_fault = 0

    for mem in listframes_fifo:
        print(mem)

    print("----------------------------------")
    # inicializa a memoria com frames
    for mem in range(len(mem_list)):
        for frame in listframes_fifo:
            if mem_list[mem][1] == 0:
                page_fault += 1
                mem_list[mem][0] = frame['id']
                mem_list[mem][1] = frame['ref']
                listframes_fifo.remove(frame)

    for mem in mem_list:
        print(mem)
    first_refer = min(mem_list)
    position = mem_list.index(first_refer)

    mem_list[position][0] = listframes_fifo[0]['id']
    mem_list[position][1] = listframes_fifo[0]['ref']
    # print(first_refer)
    # print(position)
    print("----------------------------------")
    for mem in mem_list:
        print(mem)


    print("page_fault")
    print(page_fault)





