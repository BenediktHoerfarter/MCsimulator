# MCsimulator

MCsimulator is a Monte Carlo (MC) simulation tool designed to model van der Waals systems containing Ar and/or Xe. This repository provides an MC framework for running simulations and thereby obtaining trajectories.

**This is a proof-of-concept repo and therefore neither highly optimized nor, by no means, intended for professional/scientific application!**

## Usage

1. Define your simulation parameters in the `mcsim.in`:
    - `restart_file`: Name of the restart file (i.e., an '.xyz' file)
    - `parameter_file`: Name of the parameter file (i.e., 'params_mcsim.in') containing Lennard-Jones 12-6 parameters
    - `n_steps`: Number of MC step attempts in the simulation
    - `temp`: Temperature for the Metropolis acceptance criterion
    - `vdW_cutoff`: (optional) van der Waals cutoff 
    - `seed`: (optional) Random seed for reproducibility

2. Run the MC simulation:
    ```bash
    python -m MCsimulator mcsim.in
    ```

3. Examine the obtained trajectory visually, e.g., using VMD or PyMOL.

## License

This project is licensed under the [MIT License](LICENSE).

## To-Do

- Refactoring functions
- Append/Overwrite modes and user-defined naming for trajectory file
- Naming conventions (e.g., camel case vs. underscores)
- Building interface with open-source GNN potentials for calculating energy/forces as alternative to LJ potential
