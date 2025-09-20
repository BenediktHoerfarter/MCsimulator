import sys
import numpy as np
import re
import _io

# Idea, To-Do:
# For different types of calculations (LJ-based MC, NNP-based MC, etc.):
# Create a superclass InputExtractor
# Create subclasses for each type of calculation (LJInputExtractor, NNPInputExtractor, etc.) that inherit the general methods from InputExtractor


def getStringFromEqualsignToSemicolon(inputstring: str, query: str) -> str | None:
    searchStringPos: int = inputstring.find(query)
    if searchStringPos != -1:
        searchStringPosStart: int = inputstring.find("=", searchStringPos)
        searchStringPosEnd: int = inputstring.find(";", searchStringPos)
        extractedString: str = inputstring[
            searchStringPosStart + 1 : searchStringPosEnd
        ].strip()
        return extractedString
    else:
        return None


class InputExtractor:

    def __init__(self) -> None:

        self.inputfileName: str = sys.argv[1]
        print("Reading in the input file:", self.inputfileName)

        inputfileString: str = open(self.inputfileName, "r").read()
        self.inputfileString = inputfileString

        self.restartfileFhand = self.restartfileReader()
        self.atomsWithCoordinatesList: list = (
            self.extractRestartfileAtomsWithCoordinatesList()
        )
        self.nAtoms: int = self.extractNumAtoms()
        self.parameterString: str = self.parameterStringReader()
        self.outputname: str = self.outputnameReader()
        self.nSteps: int = self.nStepsReader()
        self.temp: float = self.tempReader()
        self.vdWCutoff: float = self.vdWCutoffReader()
        self.randomseed: int = self.randomseedReader()

    def restartfileReader(self) -> _io.TextIOWrapper | None:
        restartfile = getStringFromEqualsignToSemicolon(
            self.inputfileString, "restart_file ="
        )
        try:
            restartfileFhand = open(restartfile, "r")
            print("    Using restart file:", restartfile)
            return restartfileFhand
        except:
            print(
                '|||||||||||||||||||| MC Simulator exited with ERROR ||||||||||||||||||||\nThe specified restart file could not be found!\nPlease check the filename and its path.\n    Syntax: "restart_file = ...;"'
            )
            exit()

    def extractRestartfileAtomsWithCoordinatesList(self) -> list:
        atomsWithCoordinatesList: list = []
        lineCounter: int = 0
        for line in self.restartfileFhand:
            lineCounter += 1
            if re.match(r"^[A-Z]", line) and lineCounter > 2:
                line = line.strip()
                atomsWithCoordinatesList.append(line.split())
        for atom in atomsWithCoordinatesList:
            atom[1] = float(atom[1])
            atom[2] = float(atom[2])
            atom[3] = float(atom[3])
        return atomsWithCoordinatesList

    def extractNumAtoms(self) -> int:
        numAtoms: int = len(self.atomsWithCoordinatesList)
        return numAtoms

    def parameterStringReader(self) -> str:
        parameterfile = getStringFromEqualsignToSemicolon(
            self.inputfileString, "parameter_file ="
        )
        try:
            parameterString: str = open(parameterfile, "r").read()
            print("    Using parameter file:", parameterfile)
            return parameterString
        except:
            print(
                '|||||||||||||||||||| MC Simulator exited with ERROR ||||||||||||||||||||\nThe specified parameter file could not be found!\nPlease check the filename and its path.\n    Syntax: "parameter_file = ...;"'
            )
            exit()

    def outputnameReader(self) -> str:
        outputname = getStringFromEqualsignToSemicolon(
            self.inputfileString, "output_file ="
        )        
        if outputname != None:
            print("    Writing to output file:", outputname)
            return outputname
        else:
            print("    Writing to output file: mcsim-traj.xyz")
            return "mcsim-traj.xyz"

    def nStepsReader(self) -> int:
        nSteps = getStringFromEqualsignToSemicolon(
            self.inputfileString, "n_steps ="
        )
        try:
            nSteps = int(nSteps)
            return nSteps
        except:
            print(
                '|||||||||||||||||||| MC Simulator exited with ERROR ||||||||||||||||||||\nPlease define the number of MC steps in the input file!\n    Syntax: "n_steps = ...;"'
            )
            exit()

    def tempReader(self) -> float:
        temp = getStringFromEqualsignToSemicolon(
            self.inputfileString, "temp ="
        )
        try:
            temp = float(temp)
            return temp
        except:
            temp: float = 298.15
            print(
                "||| Warning ||| --- No input temperature specified, using default value (298.15 K)."
            )
            return temp

    def vdWCutoffReader(self) -> float:
        vdWCutoff = getStringFromEqualsignToSemicolon(
            self.inputfileString, "vdW_cutoff ="
        )
        try:
            vdWCutoff = float(vdWCutoff)
            return vdWCutoff
        except:
            vdWCutoff: float = np.infty
            print(
                "||| Warning ||| --- No input van der Waals cutoff specified, using default value (no cutoff)."
            )
            return vdWCutoff

    def randomseedReader(self) -> int | None:
        randomseed = getStringFromEqualsignToSemicolon(
            self.inputfileString, "seed ="
        )
        try:
            randomseed = int(randomseed)
            print("    Using random seed:", randomseed)
            return randomseed        
        except:
            return None
