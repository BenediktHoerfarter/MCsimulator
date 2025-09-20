def lennard_jones_energy(A_lj, B_lj, distance) -> float:
    return (1 / distance**6) * ((A_lj / distance**6) + B_lj)


def energy_calculator_and_list_append(InputExtractorObject) -> list:
    atoms_with_coordinates_list = InputExtractorObject.atoms_with_coordinates_list
    parameter_string = InputExtractorObject.parameter_string
    vdW_cutoff = InputExtractorObject.vdW_cutoff
    E_pot_total: float = 0.0
    E_list: list = []
    for atomA in atoms_with_coordinates_list:
        atomA_x: float = atomA[1]
        atomA_y: float = atomA[2]
        atomA_z: float = atomA[3]
        atomA_position: int = parameter_string.find("*" + atomA[0] + "*")
        A_LJ_position: int = parameter_string.find("A_lj", atomA_position)
        A_LJ_position_start: int = parameter_string.find("=", A_LJ_position)
        A_LJ_position_end: int = parameter_string.find(";", A_LJ_position)
        A_lj: float = float(
            parameter_string[A_LJ_position_start + 1 : A_LJ_position_end].strip()
        )
        for atomB in atoms_with_coordinates_list:
            if atomB == atomA:
                continue
            else:
                atomB_x: float = atomB[1]
                atomB_y: float = atomB[2]
                atomB_z: float = atomB[3]
                square_distance: float = (
                    (atomA_x - atomB_x) ** 2
                    + (atomA_y - atomB_y) ** 2
                    + (atomA_z - atomB_z) ** 2
                )
                if square_distance <= vdW_cutoff**2:
                    atomB_position: int = parameter_string.find(
                        atomB[0] + ":", atomA_position
                    )
                    B_LJ_position: int = parameter_string.find("B_lj", atomB_position)
                    B_LJ_position_start: int = parameter_string.find("=", B_LJ_position)
                    B_LJ_position_end: int = parameter_string.find(";", B_LJ_position)
                    B_lj: float = float(
                        parameter_string[
                            B_LJ_position_start + 1 : B_LJ_position_end
                        ].strip()
                    )
                    distance: float = square_distance ** (1 / 2)
                    E_pot_total: float = E_pot_total + lennard_jones_energy(
                        A_lj, B_lj, distance
                    )
    E_list.append(E_pot_total)
    return E_list


def gen_string_of_atoms_with_coordinates_for_xyz(inputlist_atomswithcoordinates) -> str:
    input_list = inputlist_atomswithcoordinates
    number_of_atoms = len(input_list)
    string_of_atoms_with_coordinates_for_xyz: str = ""
    for i in range(number_of_atoms):
        string_of_atoms_with_coordinates_for_xyz = (
            string_of_atoms_with_coordinates_for_xyz
            + input_list[int(f"{i}")][0]
            + " "
            + str(input_list[int(f"{i}")][1])
            + " "
            + str(input_list[int(f"{i}")][2])
            + " "
            + str(input_list[int(f"{i}")][3])
            + "\n"
        )
    return string_of_atoms_with_coordinates_for_xyz
