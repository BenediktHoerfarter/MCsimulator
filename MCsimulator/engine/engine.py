import numpy as np
import random
import copy
import re

from ..utils.utils import ljEnergyCalculator, genStringAtomsWithCoordinatesForXYZ
from ..constants.constants import *


def runningMCLoop(InputExtractorObject) -> None:

    nSteps = InputExtractorObject.nSteps
    atomsWithCoordinatesList = InputExtractorObject.atomsWithCoordinatesList
    nAtoms = InputExtractorObject.nAtoms
    parameterString = InputExtractorObject.parameterString
    outputname = InputExtractorObject.outputname
    temp = InputExtractorObject.temp
    vdWCutoff = InputExtractorObject.vdWCutoff
    Elist = [ljEnergyCalculator(atomsWithCoordinatesList, parameterString, vdWCutoff)]

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
            str(nAtoms)
            + "\n"
            + "\tRead-and-Write File (.rwf)"
            + "\n"
            + genStringAtomsWithCoordinatesForXYZ(trialAtomsWithCoordinatesList)
        )
        readwritefile = open("read-write-file.rwf", "w")
        readwritefile.write(nextStepStructureString)
        readwritefile.close()
        readwritefile = open("read-write-file.rwf", "r")

        trialAtomsWithCoordinatesList: list = []
        lineCounter: int = 0
        for line in readwritefile:
            lineCounter += 1
            if (re.match(r"^[A-Z]", line) and lineCounter > 2):
                line = line.strip()
                trialAtomsWithCoordinatesList.append(line.split())
        for atom in trialAtomsWithCoordinatesList:
            atom[1] = float(atom[1])
            atom[2] = float(atom[2])
            atom[3] = float(atom[3])

        Elist.append(
            ljEnergyCalculator(
                trialAtomsWithCoordinatesList, parameterString, vdWCutoff
            )
        )

        if np.exp(
            -(Elist[-1] - Elist[-2]) * KCAL_TO_J / (IDEAL_GAS_CONST * temp)
        ) >= random.uniform(0, 1):
            structure_string: str = (
                str(nAtoms)
                + "\n"
                + "\tStep: "
                + str(stepCounter)
                + ". Total Energy: "
                + str(Elist[-1])
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
