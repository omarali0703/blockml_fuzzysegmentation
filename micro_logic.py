import sys
import os
from python_micrologic import RS3_Parser as rs3parser
from python_micrologic import SLSeg_Parser as slsegparser
from xml.etree.ElementTree import ParseError


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


args = sys.argv
print(args)

functions = ['slseg', 'rs3parse', 'rs3trainingdata',
    'rs3originaltext', 'validateboundaries']
function_called = args[1]
location = args[2]
variables = args[3:6]
number_of_docs_to_parse_index = 0
error = ''
try:

    list_path = os.listdir(location)
    print(variables)
    print(location)
    if function_called not in functions:
        print(f'{bcolors.WARNING}Incorrect function.')
        raise
    elif function_called == functions[0]:  # slseg
        print(f'{bcolors.OKGREEN}Begin parsing SLSeg...')
        # print (list_path)
        for segfile in list_path:
            abs_location = os.path.join(location, segfile)
            if os.path.isdir(abs_location):
                continue
            print(bcolors.OKBLUE+abs_location)
            slsegparser.parse_slseg(abs_location, *variables)
    elif function_called == functions[1]:  # rs3parse
        print(f'{bcolors.OKGREEN}Begin parsing RS3 Parsing...')
        for segfile in list_path:
            abs_location = os.path.join(location, segfile)
            if os.path.isdir(abs_location):
                continue
            print(f'Parsing {segfile}')
            rs3parser.parse_rs3(abs_location, *variables)
    elif function_called == functions[2]:  # rs3parse to dat file for training
        from preprocess_fis.block_text_tilling import *

        print(f'{bcolors.OKCYAN}Begin generating RS3 training data...')
        number_of_docs_to_parse = args[4]
        for segfile in list_path:
            if number_of_docs_to_parse_index < int(number_of_docs_to_parse):
                abs_location = os.path.join(location, segfile)

                print(f'{bcolors.OKCYAN}begin rs3 parsing... {abs_location}')
                try:
                    rs3parser.RS3_generate_fis_training_data(tile, split, abs_location, variables[0], str(
                        number_of_docs_to_parse_index), int(variables[2]))
                    print(f'{bcolors.WARNING}FINISHED PARSING... {variables}')

                except Exception as e:
                    print(f'{bcolors.FAIL}Failed to parse {variables}, {e}')
                    continue

                number_of_docs_to_parse_index += 1
            else:
                break
    elif function_called == functions[3]:

        print(f'{bcolors.OKCYAN}Begin generating original text from RS3...')
        for segfile in list_path:
            abs_location = os.path.join(location, segfile)
            print(abs_location)
            rs3parser.get_original_text(abs_location,  variables[0])
    elif function_called == functions[4]:
        from results.block_validators import *

        print(f'{bcolors.OKCYAN}Begin validating boundaries at selected directories...')
        ref_comp_pairs = {}
        for segfile in list_path:
            abs_location = os.path.join(location, segfile)
            filename = segfile.split('.')
            file_extension = filename[1]
            filename = filename[0]

            if file_extension in ['txt', 'rs3']:
                file_contents = open(abs_location, "r").read()
                ref_comp_pairs[filename] = [file_contents]
        print (f"Computed boundaries loaded...\n{ref_comp_pairs}")

        print(f'{bcolors.OKCYAN}Loading calculated boundaries from {variables[0]}...')
        list_path = os.listdir(variables[0])
        for segfile in list_path:
            abs_location = os.path.join(variables[0], segfile)
            filename = segfile.split('.')
            file_extension = filename[1]
            filename = filename[0]

            if file_extension in ['txt', 'rs3']:
                file_contents = open(abs_location, "r").read()
                if filename not in ref_comp_pairs:
                    print(
                        f"{bcolors.FAIL}Error parsing: computed file {filename}, doesn't have a counterpart in the reference boundary directory.")
                    raise
                ref_comp_pairs[filename].append(file_contents)

        win_diff = 0
        win_pr = 0, 0, 0
        basic_met = 0, 0, 0
        for boundary_pairs in ref_comp_pairs:
            pairs = ref_comp_pairs[boundary_pairs]
            reference_pair = pairs[0]
            calculated_pair = pairs[1]
            calc_win_diff = window_diff(reference_pair, calculated_pair, k=1, boundary="1")
            calc_win_pr = window_pr(calculated_pair, reference_pair, boundary="1")
            calc_basic_metric = basic_metric(calculated_pair, reference_pair, boundary="1")
            print(calc_win_diff, calc_win_pr, calc_basic_metric)
            win_diff += calc_win_diff
            win_pr = tuple(map(lambda i, j: i+j, basic_met, calc_win_pr))
            basic_met = tuple(map(lambda i, j: i+j, basic_met, calc_basic_metric))
        
        win_pr = tuple(map(lambda i: i/len(ref_comp_pairs), win_pr))
        basic_met = tuple(map(lambda i: i/len(ref_comp_pairs), basic_met))
        win_diff = win_diff/len(ref_comp_pairs)

        print (f"{bcolors.OKGREEN}Window Diff: {win_diff}")
        print (f"{bcolors.OKGREEN}Basic Metric: {basic_met}")
        print (f"{bcolors.OKGREEN}Window PR: {win_pr}")

except OSError as error:
    print(f"{bcolors.FAIL}Error parsing: {error}")
    sys.exit(error)
except ParseError as error:
    print (f"{bcolors.FAIL}Error parsing: {error}")
    pass
