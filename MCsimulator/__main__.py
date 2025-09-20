### This file sets up the main function
import random
from .ui.printer import printLogo, printPerformingMCRun, printNormalTermination
from .input.reader import InputExtractor
from .engine.engine import running_mc_loop


def main():

    printLogo()
    inputdata = InputExtractor()
    inputdata.restartfile_fhand_reader()
    inputdata.extract_restartfile_atoms_with_coordinates_list()
    inputdata.parameter_string_reader()
    inputdata.n_steps_reader()
    inputdata.temp_reader()
    inputdata.vdW_cutoff_reader()
    inputdata.randomseed_reader()
    inputdata.outputname_reader()
    if inputdata.randomseed != None:
        random.seed(inputdata.randomseed)
    printPerformingMCRun()
    running_mc_loop(inputdata)
    printNormalTermination()


if __name__ == "__main__":
    main()
