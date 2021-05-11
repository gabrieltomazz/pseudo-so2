
def read(infile):
    file = open(infile, "r")
    return file


def write(outfile, filename):
    filename = "arquivos/"+str(filename)+".txt"
    result = open(filename, "w+")
    result.write(outfile)
    result.close()
