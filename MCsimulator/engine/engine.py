import numpy as np
import random
import copy
import re

from ..setup.setup import (
    energyCalculatorListAppend,
    genStringAtomsWithCoordinatesForXYZ,
    ljEnergy,
)
from ..constants.constants import *


def runningMCLoop(InputExtractorObject) -> None:

    nSteps = InputExtractorObject.nSteps
    parameterString = InputExtractorObject.parameterString
    vdWCutoff = InputExtractorObject.vdWCutoff
    temp = InputExtractorObject.temp
    atomsWithCoordinatesList = InputExtractorObject.atomsWithCoordinatesList
    outputname = InputExtractorObject.outputname
    numAtoms = len(atomsWithCoordinatesList)
    Elist = energyCalculatorListAppend(InputExtractorObject)

    stepCounter: int = 0

    while stepCounter < nSteps:

        stepCounter += 1

        randomlyChosenAtom: list = random.choice(atomsWithCoordinatesList)
        randomlyChosenAtomIndex: int = atomsWithCoordinatesList.index(
            randomlyChosenAtom
        )

        trialAtomsWithCoordinatesList: list = []
        trialAtomsWithCoordinatesList = copy.deepcopy(atomsWithCoordinatesList)

        trialAtomsWithCoordinatesList[randomlyChosenAtomIndex][1] += random.uniform(
            -0.2, 0.2
        )
        trialAtomsWithCoordinatesList[randomlyChosenAtomIndex][2] += random.uniform(
            -0.2, 0.2
        )
        trialAtomsWithCoordinatesList[randomlyChosenAtomIndex][3] += random.uniform(
            -0.2, 0.2
        )

        nextStepStructureString: str = (
            str(numAtoms)
            + "\n"
            + " Read-and-Write File (.rwf)"
            + "\n"
            + genStringAtomsWithCoordinatesForXYZ(trialAtomsWithCoordinatesList)
        )
        readwritefile = open("read-write-file.rwf", "w")
        readwritefile.write(nextStepStructureString)
        readwritefile.close()
        readwritefile = open("read-write-file.rwf", "r")

        trialAtomsWithCoordinatesList: list = []
        numAtoms: int = 0
        for line in readwritefile:
            if re.match(r"^[A-Z]", line):
                line = line.strip()
                trialAtomsWithCoordinatesList.append(line.split())
                numAtoms += 1
        for atom in trialAtomsWithCoordinatesList:
            atom[1] = float(atom[1])
            atom[2] = float(atom[2])
            atom[3] = float(atom[3])

        EpotTotal: float = 0.0

        for atomA in trialAtomsWithCoordinatesList:
            atomAx: float = atomA[1]
            atomAy: float = atomA[2]
            atomAz: float = atomA[3]
            atomAPos: int = parameterString.find("*" + atomA[0] + "*")
            AljPos: int = parameterString.find("A_lj", atomAPos)
            AljPosStart: int = parameterString.find("=", AljPos)
            AljPosEnd: int = parameterString.find(";", AljPos)
            Alj: float = float(parameterString[AljPosStart + 1 : AljPosEnd].strip())
            for atomB in trialAtomsWithCoordinatesList:
                if atomB == atomA:
                    continue
                else:
                    atomBx: float = atomB[1]
                    atomBy: float = atomB[2]
                    atomBz: float = atomB[3]
                    squareDistance: float = (
                        (atomAx - atomBx) ** 2
                        + (atomAy - atomBy) ** 2
                        + (atomAz - atomBz) ** 2
                    )
                    if squareDistance <= vdWCutoff**2:
                        atomBPos: int = parameterString.find(atomB[0] + ":", atomAPos)
                        BljPos: int = parameterString.find("B_lj", atomBPos)
                        BljPosStart: int = parameterString.find("=", BljPos)
                        BljPosEnd: int = parameterString.find(";", BljPos)
                        Blj: float = float(
                            parameterString[BljPosStart + 1 : BljPosEnd].strip()
                        )
                        distance: float = squareDistance ** (1 / 2)
                        EpotTotal: float = EpotTotal + ljEnergy(Alj, Blj, distance)

        Elist.append(EpotTotal)

        if np.exp(
            -(Elist[-1] - Elist[-2]) * KCAL_TO_J / (IDEAL_GAS_CONST * temp)
        ) >= random.uniform(0, 1):
            structure_string: str = (
                str(numAtoms)
                + "\n"
                + " Step: "
                + str(stepCounter)
                + ". Total Energy: "
                + str(EpotTotal)
                + " kcal/mol."
                + "\n"
                + genStringAtomsWithCoordinatesForXYZ(trialAtomsWithCoordinatesList)
            )

            if stepCounter == 1:
                trajectoryfile = open(outputname, "w")
            else:
                trajectoryfile = open(outputname, "a")

            trajectoryfile.write(structure_string)
            trajectoryfile.close()
            atomsWithCoordinatesList: list = []
            atomsWithCoordinatesList[:] = trialAtomsWithCoordinatesList[:]
        else:
            Elist = Elist[:-1]
