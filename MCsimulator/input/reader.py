import sys
import numpy as np
import re


class InputExtractor:

    def __init__(self):

        self.inputfile_name: str = sys.argv[1]
        print("Reading in the input file:", self.inputfile_name)

        inputfile_string: str = open(self.inputfile_name, "r").read()
        self.inputfile_string = inputfile_string

        self.restartfile_fhand = None
        self.atoms_with_coordinates_list: list = None
        self.n_atoms: int = None
        self.parameter_string: str = None
        self.n_steps: int = None
        self.temp: float = None
        self.vdW_cutoff: float = None
        self.randomseed: int = None
        self.outputname: str = None

    def restartfile_fhand_reader(self) -> None:
        restartfile_position: int = self.inputfile_string.find("restart_file =")
        restartfile_position_start: int = self.inputfile_string.find(
            "=", restartfile_position
        )
        restartfile_position_end: int = self.inputfile_string.find(
            ";", restartfile_position
        )
        restartfile: str = self.inputfile_string[
            restartfile_position_start + 1 : restartfile_position_end
        ].strip()
        restartfile_fhand = open(restartfile, "r")
        print("    Using restart file:", restartfile)
        self.restartfile_fhand = restartfile_fhand

    def extract_restartfile_atoms_with_coordinates_list(self) -> None:
        atoms_with_coordinates_list: list = []
        for line in self.restartfile_fhand:
            if re.match(r"^[A-Z]", line):
                line = line.strip()
                atoms_with_coordinates_list.append(line.split())
        for atom in atoms_with_coordinates_list:
            atom[1] = float(atom[1])
            atom[2] = float(atom[2])
            atom[3] = float(atom[3])
        self.atoms_with_coordinates_list = atoms_with_coordinates_list

    def parameter_string_reader(self) -> None:
        parameterfile_position: int = self.inputfile_string.find("parameter_file =")
        parameterfile_position_start: int = self.inputfile_string.find(
            "=", parameterfile_position
        )
        parameterfile_position_end: int = self.inputfile_string.find(
            ";", parameterfile_position
        )
        parameterfile: str = self.inputfile_string[
            parameterfile_position_start + 1 : parameterfile_position_end
        ].strip()
        parameter_string: str = open(parameterfile, "r").read()
        print("    Using parameter file:", parameterfile)
        self.parameter_string = parameter_string

    def n_steps_reader(self) -> None:
        n_steps_position: int = self.inputfile_string.find("n_steps =")
        if n_steps_position != -1:
            n_steps_position_start: int = self.inputfile_string.find(
                "=", n_steps_position
            )
            n_steps_position_end: int = self.inputfile_string.find(
                ";", n_steps_position
            )
            n_steps: int = int(
                self.inputfile_string[
                    n_steps_position_start + 1 : n_steps_position_end
                ].strip()
            )
            self.n_steps = n_steps
        else:
            print(
                '|||||||||||||||||||| MC Simulator exited with ERROR ||||||||||||||||||||\nPlease define the number of MC steps in the input file!\n    Syntax: "n_steps = ...;"'
            )
            exit()

    def temp_reader(self) -> None:
        temp_position: int = self.inputfile_string.find("temp")
        if temp_position != -1:
            temp_position_start: int = self.inputfile_string.find("=", temp_position)
            temp_position_end: int = self.inputfile_string.find(";", temp_position)
            temp: float = float(
                self.inputfile_string[
                    temp_position_start + 1 : temp_position_end
                ].strip()
            )
            self.temp = temp
        else:
            temp: float = 298.15
            self.temp = temp
            print(
                "||| Warning ||| --- No input temperature specified, using default value (298.15 K)."
            )

    def vdW_cutoff_reader(self) -> None:
        vdW_cutoff_position: int = self.inputfile_string.find("vdW_cutoff")
        if vdW_cutoff_position != -1:
            vdW_cutoff_position_start: int = self.inputfile_string.find(
                "=", vdW_cutoff_position
            )
            vdW_cutoff_position_end: int = self.inputfile_string.find(
                ";", vdW_cutoff_position
            )
            vdW_cutoff: float = float(
                self.inputfile_string[
                    vdW_cutoff_position_start + 1 : vdW_cutoff_position_end
                ].strip()
            )
            self.vdW_cutoff = vdW_cutoff
        else:
            vdW_cutoff: float = np.infty
            self.vdW_cutoff = vdW_cutoff
            print(
                "||| Warning ||| --- No input van der Waals cutoff specified, using default value (no cutoff)."
            )

    def randomseed_reader(self) -> None:
        randomseed_position: int = self.inputfile_string.find("seed")
        if randomseed_position != -1:
            randomseed_position_start: int = self.inputfile_string.find(
                "=", randomseed_position
            )
            randomseed_position_end: int = self.inputfile_string.find(
                ";", randomseed_position
            )
            randomseed: int = int(
                self.inputfile_string[
                    randomseed_position_start + 1 : randomseed_position_end
                ].strip()
            )
            print("    Using random seed:", randomseed)
            self.randomseed = randomseed
        else:
            return None

    def outputname_reader(self) -> None:
        outputname_position: int = self.inputfile_string.find("out")
        if outputname_position != -1:
            outputname_position_start: int = self.inputfile_string.find(
                "=", outputname_position
            )
            outputname_position_end: int = self.inputfile_string.find(
                ";", outputname_position
            )
            outputname: str = self.inputfile_string[
                outputname_position_start + 1 : outputname_position_end
            ].strip()
            self.outputname = outputname
            print("    Writing to output file:", outputname)
        else:
            self.outputname = "mcsim-traj.xyz"
            print("    Writing to output file: mcsim-traj.xyz")
