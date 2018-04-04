#!/usr/bin/env python
import argparse
import yaml
import io

import numpy as np
from pyne.mesh import Mesh, IMeshTag
from pyne.material import MaterialLibrary
from pyne.partisn import write_partisn_input, isotropic_vol_source
from pyne.dagmc import discretize_geom, load, cell_material_assignments
from pyne import nucname
from pyne.bins import pointwise_collapse
from pyne.alara import calc_eta, calc_T


config_filename = 'config.yml'

config = \
"""
# If 'True', all intermediate files created while running the script will be removed.
# Leave blank if you which to retain all intermediate files.
clean: True

# Assess all materials in geometry for compatibility with SNILB criteria
step0:
    # Path to hdf5 geometry file for SNILB check. This is the geometry laden
    # file that will be used for activation. Note that this is the same file
    # that will be used for step 2.
    geom_file: 
    # Path to processed nuclear data.
    # (directory containing nuclib, fendl2.0bin.lib, fendl2.0bin.gam)
    data_dir: 
    # Number of photon energy groups. This should be compatible with the dose
    # rate conversion library. (24 or 42), default is 42.
    p_groups: 42
    # Single pulse irradiation time [s].
    irr_time: 
    # Single decay time of interest [s].
    decay_time: 

# Prepare PARTISN input file for adjoint photon transport
step1: 

# Calculate T matrix for each material
step2:
    # If 'True', proper background and burnup corrctions based on calculated eta
    # in step 0 will be applied to the calculated T matrix.
    # Leave blank if you want to calculate T matrix without corrections.
    correct: True
    # Path to the eta file produced in step 0.
    # change only if the file has been manually renamed or moved.
    eta_0: step0_eta.npy

# Calculate adjoint neutron source
step3: 

# Prepare PARTISN input for adjoint neutron transport
step4: 

# Generate Monte Carlo variance reduction parameters
# (biased source and weight windows)
step5: 


"""


def setup():
    """
    This function generates a blank config.yml file for the user to 
    fill in with problem specific values.
    """
    with open(config_filename, 'w') as f:
        f.write(config)
    print('File "{}" has been written'.format(config_filename))
    print('Fill out the fields in this file then run ">> gtcadis.py step0"')


def step2(cfg0, cfg2, clean):
    """
    This function calculates the T matrix for each material, n group, p group, and
    decay time.
    
    Parameters
    ----------
    cfg0 : dictionary
        User input for step 0 from the config.yml file
    cfg2: dictionary
        User input for step 2 from config.yml file
    clean: str
        User input for condition on retaining the intermediate files
    """
    # Get user input from config file
    geom = cfg0['geom_file']
    data_dir = cfg0['data_dir']
    irr_times = [cfg0['irr_time']]
    decay_times = [cfg0['decay_time']]
    num_p_groups = cfg0['p_groups']
    correct_T = cfg2['correct']
    eta_0 = cfg2['eta_0']
    
    # Define a flat, 175 group neutron spectrum, with magnitude 1E12 [n/s]
    neutron_spectrum = [1]*175  # will be normalized
    flux_magnitudes = [1.75E14] # 1E12*175

    # Get materials from geometry file
    ml = MaterialLibrary(geom)
    mats = list(ml.values())

    # Perform SNILB check and calculate eta
    T = calc_T(data_dir, mats, neutron_spectrum, flux_magnitudes, irr_times,
               decay_times, num_p_groups, eta_0, run_dir='step2',
               correct=bool(correct_T), remove=bool(clean))
    np.set_printoptions(threshold=np.nan)
    
    # Save numpy array
    np.save('step2_T.npy', T)


def main():
    """ 
    This function manages the setup and steps 0-5 for the GT-CADIS workflow.
    """
    gtcadis_help = ('This script automates the GT-CADIS process of \n'
                    'producing variance reduction parameters to optimize the\n'
                    'neutron transport step of the Rigorous 2-Step (R2S) method.\n')
    setup_help = ('Prints the file "config.yml" to be\n'
                  'filled in by the user.\n')
    step2_help = 'Calculates T matrix for each material in the geometry.'
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help=gtcadis_help, dest='command')

    setup_parser = subparsers.add_parser('setup', help=setup_help)
    step2_parser = subparsers.add_parser('step2', help=step2_help)

    args, other = parser.parse_known_args()
    if args.command == 'setup':
        setup()

    with open(config_filename, 'r') as f:
        cfg = yaml.load(f)
        clean = cfg['clean']
        
    if args.command == 'step2':
        step2(cfg['step0'], cfg['step2'], clean)

if __name__ == '__main__':
    main()

