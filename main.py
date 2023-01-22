import lib
import sys


def main():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = "inputFile.txt"
    reader = lib.Reader(filename)
    process = lib.TrafficControl(reader.fieldData, reader.roversPositions, reader.roversCommands)
    lib.Writer(process.rovers)


main()
