import os
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def run_hilda_segmentation(path_to_hilda_source, test_samples=None, output_test=None):
    
    path_to_hilda_source = os.path.join(path_to_slseg_source, 'hilda.py')
    parser05Aug16 = os.path.join(path_to_slseg_source, 'parser05Aug16')
    print(f'{bcolors.OKGREEN}Starting HILDA Segmentation...')
    try:
        os.system(f'python3 {path_to_slseg_source} {test_samples} -s ')
        # return os.path.join(output_test, 'step6_discoursed'), None
    except error:
        print(f'{bcolors.FAIL}{error}')