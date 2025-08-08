# MCSimulator

MCSimulator is a Monte Carlo (MC) simulation tool designed to model van der Waals systems containing Ar and/or Xe. This repository provides an MC framework for running simulations and thereby obtaining trajectories.

## Usage

1. Define your simulation parameters in the `mcsim.in`:
    - `restart_file`: Name of the restart file (i.e., an '.xyz' file)
    - `parameter_file`: Name of the parameter file (i.e., 'params_mcsim.in') containing Lennard-Jones 12-6 parameters
    - `n_steps`: Number of MC step attempts in the simulation
    - `temp`: Temperature for the Metropolis acceptance criterion
    - `vdW_cutoff`: (optional) van der Waals cutoff 

2. Run the MC simulation:
    ```bash
    python MCSimulator mcsim.in
    ```

3. View the results, e.g., using VMD (Visual Molecular Dynamics).

## License

This project is licensed under the [MIT License](LICENSE).
