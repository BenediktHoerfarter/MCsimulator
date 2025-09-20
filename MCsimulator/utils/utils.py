def ljEnergy(Alj: float, Blj: float, distance: float) -> float:
    return (1 / distance**6) * ((Alj / distance**6) + Blj)


def ljEnergyCalculator(atomsWithCoordinatesList: list, parameterString: str, vdWCutoff: float) -> float:
    EpotTotal: float = 0.0

    for atomA in atomsWithCoordinatesList:
        atomAx: float = atomA[1]
        atomAy: float = atomA[2]
        atomAz: float = atomA[3]
        atomAPos: int = parameterString.find("*" + atomA[0] + "*")
        AljPos: int = parameterString.find("A_lj", atomAPos)
        AljPosStart: int = parameterString.find("=", AljPos)
        AljPosEnd: int = parameterString.find(";", AljPos)
        Alj: float = float(parameterString[AljPosStart + 1 : AljPosEnd].strip())
        for atomB in atomsWithCoordinatesList:
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
    return EpotTotal


def genStringAtomsWithCoordinatesForXYZ(inputListAtomsWithCoordinates: list) -> str:
    inputList = inputListAtomsWithCoordinates
    numAtoms = len(inputList)
    stringAtomsWithCoordinatesForXYZ: str = ""
    for i in range(numAtoms):
        stringAtomsWithCoordinatesForXYZ = (
            stringAtomsWithCoordinatesForXYZ
            + inputList[int(f"{i}")][0]
            + " "
            + str(inputList[int(f"{i}")][1])
            + " "
            + str(inputList[int(f"{i}")][2])
            + " "
            + str(inputList[int(f"{i}")][3])
            + "\n"
        )
    return stringAtomsWithCoordinatesForXYZ
