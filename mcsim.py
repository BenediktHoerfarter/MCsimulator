import sys
import re
import random
import numpy as np



##################################### READING IN FILES #####################################

print('''
  MC Simulator      

M       M   CCCCCCC
MM     MM  C     
M M   M M  C     
M  M M  M  C     
M   M   M  C     
M       M  C     
M       M   CCCCCCC
           
      ''')

### reading in the input file
input_file: str = sys.argv[1]
input_string: str = open(input_file, 'r').read()
print('Reading in the input file:',input_file)

### specify restart file
restart_file_position: int = input_string.find('restart_file')
restart_file_position_start: int = input_string.find('=', restart_file_position)
restart_file_position_end: int = input_string.find(';', restart_file_position)
restart_file: str = input_string[restart_file_position_start+1:restart_file_position_end].strip()
restart_file_fhand = open(restart_file, 'r')
print('    Using restart file:',restart_file)

### specify parameter file
parameter_file_position: int = input_string.find('parameter_file')
parameter_file_position_start: int = input_string.find('=', parameter_file_position)
parameter_file_position_end: int = input_string.find(';', parameter_file_position)
parameter_file: str = input_string[parameter_file_position_start+1:parameter_file_position_end].strip()
parameter_string: str = open(parameter_file, 'r').read()
print('    Using parameter file:',parameter_file)

print('''
      
>>>> Setting up MONTE CARLO run... <<<<     
      
      ''')

### reading in the number of steps
try:
    n_steps_position: int = input_string.find('n_steps')
    n_steps_position_start: int = input_string.find('=', n_steps_position)
    n_steps_position_end: int = input_string.find(';', n_steps_position)
    n_steps: int = int(input_string[n_steps_position_start+1:n_steps_position_end].strip())
except:
    print('|||||||||||||||||||| MC Simulator exited with ERROR ||||||||||||||||||||\nPlease define the number of MC steps in the input file!\n    Syntax: "n_steps = ..."')
    quit

try:
    temp_position: int = input_string.find('temp')
    temp_position_start: int = input_string.find('=', temp_position)
    temp_position_end: int = input_string.find(';', temp_position)
    temp: float = float(input_string[temp_position_start+1:temp_position_end].strip())
except:
    temp: float = 298.15

### reading in the van der Waals cutoff
try:
    vdW_cutoff_position: int = input_string.find('vdW_cutoff')
    vdW_cutoff_position_start: int = input_string.find('=', vdW_cutoff_position)
    vdW_cutoff_position_end: int = input_string.find(';', vdW_cutoff_position)
    vdW_cutoff: float = float(input_string[vdW_cutoff_position_start+1:vdW_cutoff_position_end].strip())
except:
    vdW_cutoff: float = 12.0



##################################### SETTING UP MC RUN #####################################

### generation of a list of all atoms incl. coordinates
atoms_with_coordinates_list: list = []
number_of_atoms: int = 0
for line in restart_file_fhand:
    if re.match(r'^[A-Z]', line):
        line = line.strip()
        atoms_with_coordinates_list.append(line.split())
        number_of_atoms += 1
for atom in atoms_with_coordinates_list:
    atom[1] = float(atom[1])
    atom[2] = float(atom[2])
    atom[3] = float(atom[3])

### energy calculation
E_pot_total: float = 0.0
E_list: list = []

def lennard_jones_energy(A_lj, B_lj, distance) -> float:
    return (1 / distance**6) * ((A_lj / distance**6) + B_lj)

for atomA in atoms_with_coordinates_list:
    atomA_x: float = atomA[1]
    atomA_y: float = atomA[2]
    atomA_z: float = atomA[3]
    atomA_position: int = parameter_string.find('*'+atomA[0]+'*')
    A_LJ_position: int = parameter_string.find('A_lj', atomA_position)
    A_LJ_position_start: int = parameter_string.find('=', A_LJ_position)
    A_LJ_position_end: int = parameter_string.find(';', A_LJ_position)
    A_lj: float = float(parameter_string[A_LJ_position_start+1:A_LJ_position_end].strip())
    for atomB in atoms_with_coordinates_list:
        if atomB == atomA:
            continue
        else:
            atomB_x: float = atomB[1]
            atomB_y: float = atomB[2]
            atomB_z: float = atomB[3]
            square_distance: float = (atomA_x - atomB_x)**2 + (atomA_y - atomB_y)**2 + (atomA_z - atomB_z)**2
            if square_distance <= vdW_cutoff**2:
                atomB_position: int = parameter_string.find(atomB[0]+':', atomA_position)
                B_LJ_position: int = parameter_string.find('B_lj', atomB_position)
                B_LJ_position_start: int = parameter_string.find('=', B_LJ_position)
                B_LJ_position_end: int = parameter_string.find(';', B_LJ_position)
                B_lj: float = float(parameter_string[B_LJ_position_start+1:B_LJ_position_end].strip())
                distance: float = square_distance**(1/2)
                E_pot_total: float = E_pot_total + lennard_jones_energy(A_lj, B_lj, distance)

E_list.append(E_pot_total)

def print_atoms_with_coordinates_for_xyz_file() -> str:
    string_of_atoms_with_coordinates_for_xyz: str = ''
    for i in range(number_of_atoms):
        string_of_atoms_with_coordinates_for_xyz = string_of_atoms_with_coordinates_for_xyz + atoms_with_coordinates_list[int(f'{i}')][0] + ' ' + str(atoms_with_coordinates_list[int(f'{i}')][1]) + ' ' + str(atoms_with_coordinates_list[int(f'{i}')][2]) + ' ' + str(atoms_with_coordinates_list[int(f'{i}')][3]) + '\n'
    return string_of_atoms_with_coordinates_for_xyz
def print_trial_atoms_with_coordinates_for_xyz_file() -> str:
    string_of_atoms_with_coordinates_for_xyz: str = ''
    for i in range(number_of_atoms):
        string_of_atoms_with_coordinates_for_xyz = string_of_atoms_with_coordinates_for_xyz + trial_atoms_with_coordinates_list[int(f'{i}')][0] + ' ' + str(trial_atoms_with_coordinates_list[int(f'{i}')][1]) + ' ' + str(trial_atoms_with_coordinates_list[int(f'{i}')][2]) + ' ' + str(trial_atoms_with_coordinates_list[int(f'{i}')][3]) + '\n'
    return string_of_atoms_with_coordinates_for_xyz

structure_string: str = str(number_of_atoms) + '\n' + ' Step: 0. Total Energy: ' + str(E_pot_total) + ' kcal/mol.' + '\n' + print_atoms_with_coordinates_for_xyz_file()

trajectoryfile = open('mcsim-traj.xyz', 'a')
trajectoryfile.write(structure_string)
trajectoryfile.close()


##################################### MAKING MC STEPS - while loop #####################################

step_counter: int = 0

### random movement of one randomly chosen atom

while step_counter <= n_steps:
    
    step_counter += 1

    randomly_chosen_atom: list = random.choice(atoms_with_coordinates_list)
    randomly_chosen_atom_index: int = atoms_with_coordinates_list.index(randomly_chosen_atom)

    trial_atoms_with_coordinates_list: list = atoms_with_coordinates_list[:]
    trial_atoms_with_coordinates_list[randomly_chosen_atom_index][1] = atoms_with_coordinates_list[randomly_chosen_atom_index][1] + random.uniform(-0.5, 0.5)
    trial_atoms_with_coordinates_list[randomly_chosen_atom_index][2] = atoms_with_coordinates_list[randomly_chosen_atom_index][2] + random.uniform(-0.5, 0.5)
    trial_atoms_with_coordinates_list[randomly_chosen_atom_index][3] = atoms_with_coordinates_list[randomly_chosen_atom_index][3] + random.uniform(-0.5, 0.5)

    next_step_structure_string: str = str(number_of_atoms) + '\n' + ' Total Energy: not yet known' + '\n' + print_trial_atoms_with_coordinates_for_xyz_file()
    readwritefile = open('read-write-file.rwf', 'w')
    readwritefile.write(next_step_structure_string)
    readwritefile.close()
    readwritefile = open('read-write-file.rwf', 'r')

    next_step_atoms_with_coordinates_list: list = []
    number_of_atoms: int = 0
    for line in readwritefile:
        if re.match(r'^[A-Z]', line):
            line = line.strip()
            next_step_atoms_with_coordinates_list.append(line.split())
            number_of_atoms += 1
    for atom in next_step_atoms_with_coordinates_list:
        atom[1] = float(atom[1])
        atom[2] = float(atom[2])
        atom[3] = float(atom[3])

    E_pot_total: float = 0.0

    for atomA in next_step_atoms_with_coordinates_list:
        atomA_x: float = atomA[1]
        atomA_y: float = atomA[2]
        atomA_z: float = atomA[3]
        atomA_position: int = parameter_string.find('*'+atomA[0]+'*')
        A_LJ_position: int = parameter_string.find('A_lj', atomA_position)
        A_LJ_position_start: int = parameter_string.find('=', A_LJ_position)
        A_LJ_position_end: int = parameter_string.find(';', A_LJ_position)
        A_lj: float = float(parameter_string[A_LJ_position_start+1:A_LJ_position_end].strip())
        for atomB in next_step_atoms_with_coordinates_list:
            if atomB == atomA:
                continue
            else:
                atomB_x: float = atomB[1]
                atomB_y: float = atomB[2]
                atomB_z: float = atomB[3]
                square_distance: float = (atomA_x - atomB_x)**2 + (atomA_y - atomB_y)**2 + (atomA_z - atomB_z)**2
                if square_distance <= vdW_cutoff**2:
                    atomB_position: int = parameter_string.find(atomB[0]+':', atomA_position)
                    B_LJ_position: int = parameter_string.find('B_lj', atomB_position)
                    B_LJ_position_start: int = parameter_string.find('=', B_LJ_position)
                    B_LJ_position_end: int = parameter_string.find(';', B_LJ_position)
                    B_lj: float = float(parameter_string[B_LJ_position_start+1:B_LJ_position_end].strip())
                    distance: float = square_distance**(1/2)
                    E_pot_total: float = E_pot_total + lennard_jones_energy(A_lj, B_lj, distance)

    E_list.append(E_pot_total)

    if np.exp(-(E_list[step_counter] - E_list[step_counter-1])*4184/(8.31446261815324*temp)) >= random.uniform(0, 1):
        structure_string: str = str(number_of_atoms) + '\n' + ' Step: ' + str(step_counter) + '. Total Energy: ' + str(E_pot_total) + ' kcal/mol.' + '\n' + print_atoms_with_coordinates_for_xyz_file()
        trajectoryfile = open('mcsim-traj.xyz', 'a')
        trajectoryfile.write(structure_string)
        trajectoryfile.close()
        atoms_with_coordinates_list[:] = trial_atoms_with_coordinates_list[:]
    else:
        E_list[-1] = E_list[-2]
        continue

print(E_list)