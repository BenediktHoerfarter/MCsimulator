### This file sets up the main function
import random
from .ui.printer import logo, performing_MCrun, normal_termination
from .input.reader import InputExtractor
from .engine.engine import running_mc_loop


def main():

    logo()
    inputdata = InputExtractor()
    inputdata.extract_restartfile_fhand()
    inputdata.extract_restartfile_atoms_with_coordinates_list()
    inputdata.extract_parameter_string()
    inputdata.n_steps_reader()
    inputdata.temp_reader()
    inputdata.vdW_cutoff_reader()
    inputdata.extract_randomseed()
    if inputdata.randomseed != None:
        random.seed(inputdata.randomseed)
    performing_MCrun()
    running_mc_loop(inputdata)
    normal_termination()


if __name__ == "__main__":
    main()
