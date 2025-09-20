### This file sets up the main function
import random
from .ui.printer import printLogo, printPerformingMCRun, printNormalTermination
from .input.reader import InputExtractor
from .engine.engine import runningMCLoop


def main():

    printLogo()
    inputdata = InputExtractor()
    inputdata.restartfileReader()
    inputdata.extractRestartfileAtomsWithCoordinatesList()
    inputdata.parameterStringReader()
    inputdata.nStepsReader()
    inputdata.tempReader()
    inputdata.vdWCutoffReader()
    inputdata.randomseedReader()
    inputdata.outputnameReader()
    if inputdata.randomseed != None:
        random.seed(inputdata.randomseed)
    printPerformingMCRun()
    runningMCLoop(inputdata)
    printNormalTermination()


if __name__ == "__main__":
    main()
