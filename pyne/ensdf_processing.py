'''This module accesses various ensdf processing tools'''

import sys, os, shutil, subprocess, tarfile
from warnings import warn
from pyne.utils import QAWarning

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

if sys.version_info[0] > 2:
    basestring = str

warn(__name__ + " is not yet QA compliant.", QAWarning)

def path_to_exe(exe_name):
    exe_path_abs, dp = os.path.split(os.path.abspath(__file__))
    exe_path_abs = os.path.join(exe_path_abs, exe_name)
    exe_path_abs = os.path.join('./',exe_path_abs)
    return exe_path_abs

def verify_download_exe(exe_path, exe_url, compressed = 0, decomp_path = '', dl_size = 0):
    if not os.path.exists(exe_path):
        print('fetching executable')
        response = urllib2.urlopen(exe_url)
        prog = 0
        CHUNK = 32 * 1024
        f = open(exe_path, 'wb')
        while True:
            chunk = response.read(CHUNK)
            prog = prog + (256)
            if not chunk: break
            f.write(chunk)
        f.close()
        # set proper permissions on newly downloaded file
        os.chmod(exe_path, 744)
        if compressed:
            tfile = tarfile.open(exe_path, 'r:gz')
            tfile.extractall(decomp_path)

def alphad(inputdict_unchecked):
    """
    This function calculates the alpha hinderance factors and theoretical half 
    lives for even even ground state transitions. (alphad readme)

    Parameters
    ----------
    Input_dictionary : dictionary
        dictionary that must have the following key-pair values:
            ensdf_input_file : input file
            output_file : file for output to be written to (doesn't have to exist)

    Notes
    -----
    Everything in input dictionary is returned if ALPHAD completes successfully.

    Full documentation explaining the details of the functionality and physics
    behind ALPHAD can be found at:
        http://www.nndc.bnl.gov/nndcscr/ensdf_pgm/analysis/alphad/readme-alphad.pdf
    """
    inputdict = {}
    input_file = inputdict_unchecked['input_file']
    report_file = inputdict_unchecked['report_file']
    rewrite_hinderance = inputdict_unchecked['rewrite_input_with_hinderance_factor']
    output_file = 'alphad.out'
    if(rewrite_hinderance == 1):    
        output_file = inputdict_unchecked['output_file'] #output file if report = yes
    exe_path = path_to_exe('alphad')
    proc = subprocess.Popen([exe_path],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    inp = input_file + '\n' + report_file + '\n' + 'Y' + '\n'
    if (rewrite_hinderance == 1):
        inp = inp + 'Y' + '\n' + output_file
    else:
        inp = inp + 'N' + '\n'
    proc.stdin.write(inp.encode('utf-8'))
    proc.communicate()[0]
    proc.stdin.close()
    return inputdict_unchecked

def delta(inputdict_unchecked):
    """
    This function calculates the best values of mixing ratios based of its analysis of
    the angular correlation and conversion coefficient data.

    Input Dictionary Required Key Pair Value:
        input_file : input ensdf file
        output_file : file for output to be written to (doesn't have to exist)

    Output Dictionary Values:
        Everything in input dictionary is returned if DELTA completes successfully.
    """
    inputdict = {}
    input_file = inputdict_unchecked['input_file']
    output_file = inputdict_unchecked['output_file']

    exe_path = path_to_exe('delta')
    proc = subprocess.Popen([exe_path],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    inp = input_file + '\n' + output_file + '\n'
    proc.stdin.write(inp.encode('utf-8'))
    proc.communicate()[0]
    proc.stdin.close()
    return inputdict_unchecked

def gabs(inputdict_unchecked):
    """
    This program calculates Gamma-ray absolute intensity and normalization (GABS readme)

    Parameters
    ----------
    Input_dictionary : dictionary
        dictionary that must have the following key-pair values:
            input_file : input ensdf file
            dataset_file : dataset file to be used
            output file : file for output to be written to (doesn't have to exist)

    Notes
    -----
    Everything in input dictionary is returned if GABS completes successfully.
    """
    exe_path = path_to_exe('gabs') 

    gabs_url = "http://www.nndc.bnl.gov/nndcscr/ensdf_pgm/analysis/gabs/unx/gabs"
    verify_download_exe(exe_path, gabs_url, dl_size = 8704)
    
    inputdict = {}
    input_file = inputdict_unchecked['input_file']
    dataset_file = inputdict_unchecked['dataset_file']
    output_file = inputdict_unchecked['output_file'] #report file << CHANGE BACK TO REPORT..

    #add option to not get new dataset (currently new dataset is hardprogrammed to yes)
    exe_path = path_to_exe('gabs')
    proc = subprocess.Popen([exe_path],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    inp = input_file + '\n' + output_file + '\n' + 'Y' + '\n' + dataset_file
    proc.stdin.write(inp.encode('utf-8'))
    proc.communicate()[0]
    proc.stdin.close()

<<<<<<< 65c46cdb7aa26efcc3c8440364d1f2d9a7c4093d
<<<<<<< 5227eb46c01be6dff2a90dd6c68cf5b79c837753
def gtol(inputdict_unchecked):
    """
    GTOL uses gamma-ray energies to derive a set of least-squares adjusted level energies.  The
    net feeding at each level is calculated from the input gamma intensities and conversion 
    coefficients. (GTOL readme)

    Input Dictionary Required Key Pair Value:
        input_file : input ensdf file.
        report_file : desired gtol report file path.
        new_ensdf_file_with_results : boolean, if true then a new ensdf file with results
                                      will be created.
        output_file : desired gtol output file path.
        supress_gamma_comparison : boolean, if true the gamma comparison will be suppressed.
        dcc_theory_percent : double, specifies the dcc theory percentage to be used.


    Output Dictionary Values:
        Everything in input dictionary is returned if GTOL completes successfully.
    """
    inputdict = {}
    input_file = inputdict_unchecked['input_file']
    report_file = inputdict_unchecked['report_file']
    new_out = inputdict_unchecked['new_ensdf_file_with_results']
    output_file = inputdict_unchecked['output_file'] #output file if report = yes
    supress_g = inputdict_unchecked['supress_gamma_comparison']
    supress_ic = inputdict_unchecked['supress_intensity_comparison']
    dcc_theory = inputdict_unchecked['dcc_theory_percent']

    exe_path = path_to_exe('gtol')
    proc = subprocess.Popen([exe_path],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    inp = input_file + '\n' + report_file + '\n'
    if (new_out):
        inp = inp + 'Y' + '\n' + output_file + '\n'
    else:
        inp = inp + 'N' + '\n'
    if (supress_g):
        inp = inp + 'Y' + '\n'
    else:
        inp = inp + 'N' + '\n'
    if(supress_ic):
        inp = inp + 'Y' + '\n'
    else:
        inp = inp + 'N' + '\n' + dcc_theory + '\n'
    proc.stdin.write(inp.encode('utf-8'))
    proc.communicate()[0]
    proc.stdin.close()
    return inputdict_unchecked

def hsicc(inputdict_unchecked):
    """
    This program calculates internal conversion coefficients. (HSICC readme)

    Input Dictionary Required Key Pair Value:
        data_deck : data deck to be used for hsicc program.
        icc_index : icc index to be used for hsicc program.
        icc_table : icc table to be used for the hsicc program.
        complete_report : desired report file path for hsicc program.
        new_card_deck : desired new card deck file path for hsicc program.
        comparison_report : desired comparison report path for hsicc program.
        is_multipol_known : 1 if multipol is known, 0 otherwise.

    Output Dictionary Values:
        Everything in input dictionary is returned if HSICC completes successfully.
    """
    inputdict = {}
    data_deck = inputdict_unchecked['data_deck']
    icc_index = inputdict_unchecked['icc_index']
    icc_table = inputdict_unchecked['icc_table']
    complete_report = inputdict_unchecked['complete_report']
    new_card_deck = inputdict_unchecked['new_card_deck']
    comparison_report = inputdict_unchecked['comparison_report']
    multipol_known = inputdict_unchecked['is_multipol_known'] #'Y or CR'

    exe_path = path_to_exe('hsicc')
    proc = subprocess.Popen([exe_path],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    inp = data_deck + '\n' + icc_index + '\n' + icc_table + '\n' + \
        complete_report + '\n' + new_card_deck + '\n' + comparison_report + '\n' + multipol_known
    proc.stdin.write(inp.encode('utf-8'))
    proc.communicate()[0]
    proc.stdin.close()
    return inputdict_unchecked

def hsmrg(inputdict_unchecked):
    """
    This program merges new gamma records created by HSICC with the original input 
    data.  (HSICC readme)

    Parameters
    ----------
    Input_dictionary : dictionary
        dictionary that must have the following key-pair values:
            input_data_set : path to input data file.
            output_report : desired path to output report file.
            data_table : path to data table.
            output_data_set : desired path to output data set.

    Notes
    -----
    Everything in input dictionary is returned if LOGFT completes successfully.
    """
    inputdict = {}
    data_deck = inputdict_unchecked['data_deck']
    card_deck = inputdict_unchecked['card_deck']
    merged_data_deck = inputdict_unchecked['merged_data_deck']

    exe_path = path_to_exe('hsmrg')
    proc = subprocess.Popen([exe_path],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    inp = data_deck + '\n' + card_deck + '\n' + merged_data_deck
    proc.stdin.write(inp.encode('utf-8'))
    proc.communicate()[0]
    proc.stdin.close()
    return inputdict_unchecked

def seqhst(inputdict_unchecked):
    """
    This program recreates a sequential file of the internal conversion table from the 
    direct access file.  (HSICC readme)

    Input Dictionary Required Key Pair Value:
        binary_table_input_file : binary table input file path.
        sequential_output_file : desired path of sequential output file.

    Output Dictionary Values:
        Everything in input dictionary is returned if SEQHST completes successfully.
    """
    #NOTE: changed input file line length to 90 to support longer file paths in fortran source.
    inputdict = {}
    input_file = inputdict_unchecked['binary_table_input_file']
    output_file = inputdict_unchecked['sequential_output_file']

    exe_path = path_to_exe('seqhst')
    proc = subprocess.Popen([exe_path],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    inp = input_file + '\n' + output_file
    proc.stdin.write(inp.encode('utf-8'))
    proc.communicate()[0]
    proc.stdin.close()
=======
def radd(inputdict_unchecked):
    """
    This code (RadD.FOR) deduces the radius parameter (r 0 ) for odd-odd and odd-A nuclei 
    using the even-even radii [1] as input parameters. 

    These radii deduced for odd-A and odd-odd nuclides can be used in the calculation of 
    alpha hindrance factors. In this procedure, it is assumed that radius parameter 
    ( r 0 Z , N ) for odd-Z and odd-N nuclides lies midway between the radius parameters of 
    adjacent even-even neighbors calculates reduced transition probabilities. (RADD readme)

    Parameters
    ----------
    Input_dictionary : dictionary
        dictionary that must have the following key-pair values:
            input_file : input ensdf file
            output file : file for output to be written to (doesn't have to exist)

    Notes
    -----
    Everything in input dictionary is returned if RADD completes successfully.
    """
    inputdict = {}
    atomic_number = inputdict_unchecked['atomic_number']
    neutron_number = inputdict_unchecked['neutron_number']
    output_file = inputdict_unchecked['output_file']

    # Create symlinks to the two binaries the radd executables uses.
    AK04_path = path_to_exe('98AK04.in')
    ELE_path = path_to_exe('ELE.in')
    AK04_set = False
    ELE_set = False
    if not os.path.exists('98AK04.in'):
        os.symlink(AK04_path, '98AK04.in')
        AK04_set = True
    if not os.path.exists('ELE.in'):
        os.symlink(ELE_path, 'ELE.in')
        ELE_set = True

    exe_path = path_to_exe('radd')
    inp = atomic_number + '\n' + neutron_number + '\n' + 'NO' + '\n'
    proc = subprocess.Popen([exe_path],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    proc.stdin.write(inp.encode('utf-8'))
    radd_output = proc.communicate()[0]
    proc.stdin.close()
    f = open(output_file, 'w')
    f.write(radd_output.decode("utf-8"))
    f.close()

    if AK04_set:
        os.remove('98AK04.in')
    if ELE_set:
        os.remove('ELE.in')
    return inputdict_unchecked

def ruler(inputdict_unchecked):
    """
    This program calculates reduced transition probabilities. (RULER readme)

    Parameters
    ----------
    Input_dictionary : dictionary
        dictionary that must have the following key-pair values:
            input_file : input ensdf file
            output file : file for output to be written to (doesn't have to exist)

    Notes
    -----
    Everything in input dictionary is returned if RULER completes successfully.
    """
    inputdict = {}
    input_file = inputdict_unchecked['input_file']
    output_report_file = inputdict_unchecked['output_report_file']
    mode_of_operation = inputdict_unchecked['mode_of_operation']
    assumed_dcc_theory = inputdict_unchecked['assumed_dcc_theory']
    
    exe_path = path_to_exe('ruler')
    ruler_output = subprocess.Popen([exe_path],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    inp = input_file + '\n' + output_report_file + '\n' + mode_of_operation + '\n' + assumed_dcc_theory
    ruler_output.stdin.write(inp.encode('utf-8'))
    ruler_output.communicate()[0]
    ruler_output.stdin.close()
    return inputdict_unchecked
