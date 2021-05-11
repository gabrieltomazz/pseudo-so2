import sys
import read_file

def main():

    inFile = sys.argv[1]
    file = read_file.read(inFile)

    result = open("arquivos/process_result.txt", "x")
    result.write("Write some code!")
    result.close()


if __name__ == "__main__":
    main()
