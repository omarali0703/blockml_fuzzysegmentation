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


def run_slseg(path_to_slseg_source):
    path_to_slseg_source = os.path.join(path_to_slseg_source, 'run_all.py')
    test_samples = os.path.join(path_to_slseg_source, 'test_samples')
    output_test = os.path.join(path_to_slseg_source, 'output_test')
    parser05Aug16 = os.path.join(path_to_slseg_source, 'parser05Aug16')
    print(f'{bcolors.OKGREEN}Starting SLSeg...')
    try:
        os.system(f'python3 {path_to_slseg_source} {test_samples} {output_test} {parser05Aug16} -T50')
        return os.path.join(output_test, 'step6_discoursed'), None
    except error:
        print(f'{bcolors.FAIL}{error})
        