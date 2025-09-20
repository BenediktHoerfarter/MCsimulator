import sys
import numpy as np
import re


class InputExtractor:

    def __init__(self):

        self.inputfileName: str = sys.argv[1]
        print("Reading in the input file:", self.inputfileName)

        inputfileString: str = open(self.inputfileName, "r").read()
        self.inputfileString = inputfileString

        self.restartfileFhand = None
        self.atomsWithCoordinatesList: list = None
        self.nAtoms: int = None
        self.parameterString: str = None
        self.nSteps: int = None
        self.temp: float = None
        self.vdWCutoff: float = None
        self.randomseed: int = None
        self.outputname: str = None

    def restartfileReader(self) -> None:
        restartfilePos: int = self.inputfileString.find("restart_file =")
        restartfilePosStart: int = self.inputfileString.find("=", restartfilePos)
        restartfilePosEnd: int = self.inputfileString.find(";", restartfilePos)
        restartfile: str = self.inputfileString[
            restartfilePosStart + 1 : restartfilePosEnd
        ].strip()
        restartfileFhand = open(restartfile, "r")
        print("    Using restart file:", restartfile)
        self.restartfileFhand = restartfileFhand

    def extractRestartfileAtomsWithCoordinatesList(self) -> None:
        atomsWithCoordinatesList: list = []
        for line in self.restartfileFhand:
            if re.match(r"^[A-Z]", line):
                line = line.strip()
                atomsWithCoordinatesList.append(line.split())
        for atom in atomsWithCoordinatesList:
            atom[1] = float(atom[1])
            atom[2] = float(atom[2])
            atom[3] = float(atom[3])
        self.atomsWithCoordinatesList = atomsWithCoordinatesList

    def parameterStringReader(self) -> None:
        parameterfilePos: int = self.inputfileString.find("parameter_file =")
        parameterfilePosStart: int = self.inputfileString.find("=", parameterfilePos)
        parameterfilePosEnd: int = self.inputfileString.find(";", parameterfilePos)
        parameterfile: str = self.inputfileString[
            parameterfilePosStart + 1 : parameterfilePosEnd
        ].strip()
        parameterString: str = open(parameterfile, "r").read()
        print("    Using parameter file:", parameterfile)
        self.parameterString = parameterString

    def outputnameReader(self) -> None:
        outputnamePos: int = self.inputfileString.find("output_file =")
        if outputnamePos != -1:
            outputnamePosStart: int = self.inputfileString.find("=", outputnamePos)
            outputnamePosEnd: int = self.inputfileString.find(";", outputnamePos)
            outputname: str = self.inputfileString[
                outputnamePosStart + 1 : outputnamePosEnd
            ].strip()
            self.outputname = outputname
            print("    Writing to output file:", outputname)
        else:
            self.outputname = "mcsim-traj.xyz"
            print("    Writing to output file: mcsim-traj.xyz")

    def nStepsReader(self) -> None:
        nStepsPos: int = self.inputfileString.find("n_steps =")
        if nStepsPos != -1:
            nStepsPosStart: int = self.inputfileString.find("=", nStepsPos)
            nStepsPosEnd: int = self.inputfileString.find(";", nStepsPos)
            nSteps: int = int(
                self.inputfileString[nStepsPosStart + 1 : nStepsPosEnd].strip()
            )
            self.nSteps = nSteps
        else:
            print(
                '|||||||||||||||||||| MC Simulator exited with ERROR ||||||||||||||||||||\nPlease define the number of MC steps in the input file!\n    Syntax: "n_steps = ...;"'
            )
            exit()

    def tempReader(self) -> None:
        tempPos: int = self.inputfileString.find("temp =")
        if tempPos != -1:
            tempPosStart: int = self.inputfileString.find("=", tempPos)
            tempPosEnd: int = self.inputfileString.find(";", tempPos)
            temp: float = float(
                self.inputfileString[tempPosStart + 1 : tempPosEnd].strip()
            )
            self.temp = temp
        else:
            temp: float = 298.15
            self.temp = temp
            print(
                "||| Warning ||| --- No input temperature specified, using default value (298.15 K)."
            )

    def vdWCutoffReader(self) -> None:
        vdWCutoffPos: int = self.inputfileString.find("vdWCutoff =")
        if vdWCutoffPos != -1:
            vdWCutoffPosStart: int = self.inputfileString.find("=", vdWCutoffPos)
            vdWCutoffPosEnd: int = self.inputfileString.find(";", vdWCutoffPos)
            vdWCutoff: float = float(
                self.inputfileString[vdWCutoffPosStart + 1 : vdWCutoffPosEnd].strip()
            )
            self.vdWCutoff = vdWCutoff
        else:
            vdWCutoff: float = np.infty
            self.vdWCutoff = vdWCutoff
            print(
                "||| Warning ||| --- No input van der Waals cutoff specified, using default value (no cutoff)."
            )

    def randomseedReader(self) -> None:
        randomseedPos: int = self.inputfileString.find("seed =")
        if randomseedPos != -1:
            randomseedPosStart: int = self.inputfileString.find("=", randomseedPos)
            randomseedPosEnd: int = self.inputfileString.find(";", randomseedPos)
            randomseed: int = int(
                self.inputfileString[randomseedPosStart + 1 : randomseedPosEnd].strip()
            )
            print("    Using random seed:", randomseed)
            self.randomseed = randomseed
        else:
            return None
