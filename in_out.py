import numpy
import copy
import weakref


def build(rolls):

    lastRoll = int(rolls.readline())
    initRoll = int(rolls.readline())

    print(lastRoll)
    print(initRoll)

    listRequests = read_cilindro_from_file(rolls)
    fcfs(listRequests)
    sstf(listRequests)
    scan(listRequests)


def read_cilindro_from_file(self):

    newListRools = []
    for rool in self:
        dados = int(rool)
        print(dados)
        newListRools.append(dados)

    return newListRools


def fcfs(listRequests):
    listrools_fcfs = list.copy(listRequests)
    result = numpy.diff(listrools_fcfs)
    seeks = 0
    for res in result:
        seeks = seeks + abs(res)
    print("FCFS "+str(seeks))


def sstf(listrools):
    listrools_sstf = list.copy(listrools)
    seek = 0
    min_position = listrools_sstf[0]

    while len(listrools_sstf) > 1:
        listrools_sstf.remove(min_position)
        min_seek, min_position = smallest_seek(listrools_sstf, min_position)
        seek = seek+min_seek

    print("SSTF "+str(seek))


def scan(listrools):
    listrools_scan = list.copy(listrools)
    seek = 0
    min_position = listrools_scan[0]
    listrools_scan.append(0)
    direction = 'left'

    while len(listrools_scan) > 1:
        listrools_scan.remove(min_position)
        min_seek, min_position, direction = smallest_seek_direction(listrools_scan, min_position, direction)
        seek = seek + min_seek

    print("SCAN " + str(seek))


def smallest_seek(listrools_sstf, position):
    min_seek = max(listrools_sstf)
    min_position = 0
    for rool in listrools_sstf:
        seek = abs(position - rool)
        if seek < min_seek:
            min_seek = seek
            min_position = rool

    return min_seek, min_position


def smallest_seek_direction(listrools_scan, position, direction):
    min_seek = max(listrools_scan)
    min_position = 0

    if position == 0:
        direction = 'right'

    for rool in listrools_scan:
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



