import sys
import file_manager
import process

import in_out

def main():

    # opcao do module
    moduleOption = sys.argv[1]
    # pega o arquivo
    inFile = sys.argv[2]
    # le o arquivo
    file = file_manager.read(inFile)

    if moduleOption == '1':
        process.build(file)
    elif moduleOption == '2':
        process.build(file)
    else:
        in_out.build(file)


if __name__ == "__main__":
    main()
