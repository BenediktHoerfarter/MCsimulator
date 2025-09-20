import numpy as np
import random
import copy
import re

from ..setup.setup import (
    energy_calculator_and_list_append,
    gen_string_of_atoms_with_coordinates_for_xyz,
    lennard_jones_energy,
)
from ..constants.constants import *


def running_mc_loop(InputExtractorObject) -> None:

    n_steps = InputExtractorObject.n_steps
    parameter_string = InputExtractorObject.parameter_string
    vdW_cutoff = InputExtractorObject.vdW_cutoff
    temp = InputExtractorObject.temp
    atoms_with_coordinates_list = InputExtractorObject.atoms_with_coordinates_list
    outputname = InputExtractorObject.outputname
    number_of_atoms = len(atoms_with_coordinates_list)
    E_list = energy_calculator_and_list_append(InputExtractorObject)

    step_counter: int = 0

    while step_counter < n_steps:

        step_counter += 1

        randomly_chosen_atom: list = random.choice(atoms_with_coordinates_list)
        randomly_chosen_atom_index: int = atoms_with_coordinates_list.index(
            randomly_chosen_atom
        )

        trial_atoms_with_coordinates_list: list = []
        trial_atoms_with_coordinates_list = copy.deepcopy(atoms_with_coordinates_list)

        trial_atoms_with_coordinates_list[randomly_chosen_atom_index][1] += random.uniform(-0.2, 0.2)
        trial_atoms_with_coordinates_list[randomly_chosen_atom_index][2] += random.uniform(-0.2, 0.2)
        trial_atoms_with_coordinates_list[randomly_chosen_atom_index][3] += random.uniform(-0.2, 0.2)

        next_step_structure_string: str = (
            str(number_of_atoms)
            + "\n"
            + " Read-and-Write File (.rwf)"
            + "\n"
            + gen_string_of_atoms_with_coordinates_for_xyz(
                trial_atoms_with_coordinates_list
            )
        )
        readwritefile = open("read-write-file.rwf", "w")
        readwritefile.write(next_step_structure_string)
        readwritefile.close()
        readwritefile = open("read-write-file.rwf", "r")

        trial_atoms_with_coordinates_list: list = []
        number_of_atoms: int = 0
        for line in readwritefile:
            if re.match(r"^[A-Z]", line):
                line = line.strip()
                trial_atoms_with_coordinates_list.append(line.split())
                number_of_atoms += 1
        for atom in trial_atoms_with_coordinates_list:
            atom[1] = float(atom[1])
            atom[2] = float(atom[2])
            atom[3] = float(atom[3])

        E_pot_total: float = 0.0

        for atomA in trial_atoms_with_coordinates_list:
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
            for atomB in trial_atoms_with_coordinates_list:
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
                        B_LJ_position: int = parameter_string.find(
                            "B_lj", atomB_position
                        )
                        B_LJ_position_start: int = parameter_string.find(
                            "=", B_LJ_position
                        )
                        B_LJ_position_end: int = parameter_string.find(
                            ";", B_LJ_position
                        )
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

        if np.exp(
            -(E_list[-1] - E_list[-2]) * KCAL_TO_J / (IDEAL_GAS_CONST * temp)
        ) >= random.uniform(0, 1):
            structure_string: str = (
                str(number_of_atoms)
                + "\n"
                + " Step: "
                + str(step_counter)
                + ". Total Energy: "
                + str(E_pot_total)
                + " kcal/mol."
                + "\n"
                + gen_string_of_atoms_with_coordinates_for_xyz(
                    trial_atoms_with_coordinates_list
                )
            )
            
            if step_counter == 1:
                trajectoryfile = open(outputname, "w")
            else:
                trajectoryfile = open(outputname, "a")

            trajectoryfile.write(structure_string)
            trajectoryfile.close()
            atoms_with_coordinates_list: list = []
            atoms_with_coordinates_list[:] = trial_atoms_with_coordinates_list[:]
        else:
            E_list = E_list[:-1]
