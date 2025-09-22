import random
from .ui.printer import printLogo, printPerformingMCRun, printNormalTermination
from .input.reader import InputExtractor
from .engine.engine import runningMCLoop


def main():

    printLogo()

    inputdata = InputExtractor()
    if inputdata.randomseed != None:
        random.seed(inputdata.randomseed)

    printPerformingMCRun()

    runningMCLoop(inputdata)

    printNormalTermination()


if __name__ == "__main__":
    main()
