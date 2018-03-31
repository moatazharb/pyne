#!/usr/bin/env python
import argparse
import yaml
import io

import numpy as np
from pyne.mesh import Mesh
from pyne.partisn import write_partisn_input, isotropic_vol_source
from pyne.dagmc import discretize_geom, load
from pyne import nucname
from pyne.bins import pointwise_collapse


config_filename = 'config.yml'

config = \
    """
# If 'True' all intermediate files created while running the script will be removed.
# Leave blank (not even spaces) if you which to retain all intermediate files
clean: True

# Assess all materials in geometry for compatibility with SNILB criteria
step0:
    # Path to hdf5 geometry file for SNILB check. This is the geometry laden 
    # file that will be used for activation. Note that this is the same file 
    # that will be used for step 2
    geom_file:
    # Path to processed nuclear data
    # (directory containing nuclib, fendl2.0bin.lib, fendl2.0bin.gam)               
    data_dir:
    # Number of photon energy groups. This should be compatible with the dose 
    # rate conversion library. (24 or 42), default is 42.
    p_groups: 42
    # Single pulse irradiation time                          
    irr_time:                                                                       
    # Single decay time of interest                                                 
    decay_time: 

# Prepare PARTISN input file for adjoint photon transport
step1:

# Calculate T matrix for each material
step2:

# Calculate adjoint neutron source
step3:

# Prepare PARTISN input for adjoint neutron transport
step4:

# Generate Monte Carlo variance reduction parameters
# (biased source and weight windows)
step5:


"""


def setup():
    """This function generates a blank config.yml file for the user to 
    fill in with problem specific values.
    """
    with open(config_filename, 'w') as f:
        f.write(config)
    print('File "{}" has been written'.format(config_filename))
    print('Fill out the fields in this file then run ">> gtcadis.py step0"')


def step0(cfg, clean):
    """
    This function performs the SNILB criteria check
    
    Parameters
    ----------
    cfg : dictionary
        User input for step 0 from the config.yml file
    """
    # Get user-input from config file
    geom = cfg['geom_file']
    data_dir = cfg['data_dir']
    irr_times = [cfg['irr_time']]
    decay_times = [cfg['decay_time']]
    num_p_groups = cfg['p_groups']
    
    # Define a flat, 175 group neutron spectrum, with magnitude 1E12
    neutron_spectrum = [1]*175  # will be normalized
    flux_magnitudes = [1.75E14] # 1E12*175

    # Get materials from geometry file
    ml = MaterialLibrary(geom)
    mats = list(ml.values())
    print list(ml.keys())

    # Perform SNILB check and calculate eta
    eta = calc_eta(data_dir, mats, neutron_spectrum, flux_magnitudes, irr_times,
                   decay_times, num_p_groups, run_dir='step0', remove=bool(clean))
    np.set_printoptions(threshold=np.nan)
    
    # Save numpy array that will be loaded by step 2
    np.save('step0_eta.npy', eta)


def main():
    """ This function manages the setup and steps 0-5 for the GT-CADIS workflow.
    """
    gtcadis_help = ('This script automates the GT-CADIS process of \n'
                    'producing variance reduction parameters to optimize the\n'
                    'neutron transport step of the Rigorous 2-Step (R2S) method.\n')
    setup_help = ('Prints the file "config.yml" to be\n'
                  'filled in by the user.\n')
    step0_help = 'Performs SNILB criteria check.'
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help=gtcadis_help, dest='command')

    setup_parser = subparsers.add_parser('setup', help=setup_help)
    step0_parser = subparsers.add_parser('step0', help=step0_help)

    args, other = parser.parse_known_args()
    if args.command == 'setup':
        setup()

    try open(config_filename, 'r') as f:
        cfg = yaml.load(f)
        clean = cfg['clean']
    except:
        raise NameError('config.yml file cannot be found. Please run ">>gtcadis.py setup" first.')
    if args.command == 'step0':
        step0(cfg['step0'], clean)

if __name__ == '__main__':
    main()

