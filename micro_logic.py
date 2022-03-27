import sys
import os
import json
from python_micrologic import RS3_Parser as rs3parser
from python_micrologic import SLSeg_Parser as slsegparser
from python_micrologic import SentiWordNet_Parser as sentparser

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
             'rs3originaltext', 'validateboundaries', 'clauseparse', 'generatedsmall', 'sentimentcasestudy']
function_called = args[1]
location = args[2]
variables = args[3:7]
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
                        number_of_docs_to_parse_index), int(variables[2]), parse_type=variables[3])
                    print(f'{bcolors.WARNING}FINISHED PARSING... {variables}')
                    script = "osascript -e 'tell application \"Messages\" to send \"FuzzySeg has finished creating training data.\" to buddy \"07948171108\"'"
                    os.system(script)
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
        print(f"Computed boundaries loaded...\n{ref_comp_pairs}")

        print(
            f'{bcolors.OKCYAN}Loading calculated boundaries from {variables[0]}...')
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
                    continue
                ref_comp_pairs[filename].append(file_contents)

        win_diff = 0
        win_pr = 0, 0, 0
        basic_met = 0, 0, 0
        print(ref_comp_pairs)
        total_compares = 0
        for boundary_pairs in ref_comp_pairs:
            pairs = ref_comp_pairs[boundary_pairs]
            if len(pairs) <= 1:
                continue
            reference_pair = pairs[0]
            calculated_pair = pairs[1]
            calc_win_diff = window_diff(
                reference_pair, calculated_pair, k=1, boundary="1")
            calc_win_pr = window_pr(
                calculated_pair, reference_pair, boundary="1")
            calc_basic_metric = basic_metric(
                calculated_pair, reference_pair, boundary="1")
            print(calc_win_diff, calc_win_pr, calc_basic_metric)
            total_compares += 1
            win_diff += calc_win_diff
            win_pr = tuple(map(lambda i, j: i+j, basic_met, calc_win_pr))
            basic_met = tuple(
                map(lambda i, j: i+j, basic_met, calc_basic_metric))

        win_pr = tuple(map(lambda i: i/total_compares, win_pr))
        basic_met = tuple(map(lambda i: i/total_compares, basic_met))
        win_diff = win_diff/total_compares

        print(f"{bcolors.OKGREEN}Window Diff: {win_diff}")
        print(f"{bcolors.OKGREEN}Basic Metric: {basic_met}")
        print(f"{bcolors.OKGREEN}Window PR: {win_pr}")
    elif function_called == functions[5]:
        for segfile in list_path:
            abs_location = os.path.join(location, segfile)
            filename = segfile.split('.')
            file_extension = filename[1]
            filename = filename[0]

            if file_extension in ['txt', 'rs3']:
                print(f'{bcolors.OKCYAN}Loading raw text file {segfile}...')

                file_contents = open(abs_location, "r").read()
                clause_markers = [',', '.', ]
                for marker in clause_markers:
                    file_contents = file_contents.replace(marker, '|')
                file_contents = file_contents.replace('  ', ' ')

                file_contents = file_contents.split('|')
                binary_contents = '1'
                for segments in file_contents:
                    binary_contents += f"{'0'*(len(segments.split(' ')) - 1)}1"

                binary_contents = binary_contents[:-1]

                abs_location = os.path.join(
                    variables[0], f'{filename}_sentence.txt')
                output = open(abs_location, 'w')
                output.write(binary_contents)
                print(f'{bcolors.OKCYAN}Finished parsing {segfile}...')
    elif function_called == functions[6]:
        import re
        import math
        max_block_size = int(variables[1])

        for segfile in list_path:
            block_counter = 0
            current_line = 0
            abs_location = os.path.join(location, segfile)
            filename = segfile.split('.')
            file_extension = filename[1]
            filename = filename[0]

            if file_extension in ['txt', 'rs3']:
                print(f'{bcolors.OKCYAN}Loading RST file {segfile}...')
                file_contents = open(abs_location, "r").read()
                file_contents = re.sub('<[^>]*>', '', file_contents)
                file_lines = file_contents.split('\n')
                file_lines = [f.strip() for f in file_lines]
                total_blocks = math.ceil(len(file_lines)/max_block_size)
                file_blocks = {i: [] for i in range(total_blocks)}

                for i in range(len(file_lines)):
                    if current_line == max_block_size:
                        block_counter += 1
                        current_line = 0
                    file_blocks[block_counter].append(file_lines[i])
                    current_line += 1

                print(file_blocks)

                for block in file_blocks:
                    print(f'{bcolors.OKCYAN}Processing part{block} of {filename}')
                    new_sub_file_data = file_blocks[block]
                    new_sub_file = os.path.join(
                        variables[0], f'{filename}_part{block}.txt')
                    new_sub_file = open(new_sub_file, 'w')
                    line_data = ''
                    for line in new_sub_file_data:
                        if line != '':
                            line_data += f'<segment>{line}</segment>\n'
                    new_sub_file_text = f'<rst>\n<body>\n{line_data}</body>\n</rst>\n'
                    new_sub_file.write(new_sub_file_text)
                    print(
                        f'{bcolors.OKCYAN}Finished Processing part{block} of {filename}')
    elif function_called == functions[7]:
        pre = 0 
        rec = 0
        f1 = 0
        file_counter = 0
        for segfile in list_path:
            block_counter = 0
            current_line = 0
            abs_location = os.path.join(location, segfile)
            filename = segfile.split('.')
            file_extension = filename[1]
            filename = filename[0]

            if file_extension in ['json']:
                print(f'{bcolors.OKCYAN}Loading JSON file {segfile}...')
                file_contents = open(abs_location, "r").read()
                sentiment_data = json.loads(file_contents)
                FP=0
                FN=0
                TP=0
                TN=0
                for review in sentiment_data:
                    review_sentence = review['reviewText']
                    review_reference_score = 1 if float(review['overall']) >= 2.5 else 0
                    output = sentparser.parse_sentence(review_sentence, rst=False,)
                    print (review_reference_score, output)
                    if output == 1 and review_reference_score == 1:
                        TP += 1
                    if output == 1 and review_reference_score == 0:
                        FP += 1
                    if output == 0 and review_reference_score == 0:
                        TN += 1
                    if output == 0 and review_reference_score == 1:
                        FN += 1
                
                pre += TP/(TP+FP)
                rec += TP/(TP+FN)
                f1  += 2 * (pre*rec)/(pre+rec)
            
            file_counter += 1

        pre = pre / file_counter      
        rec = rec / file_counter      
        f1 = f1 / file_counter      

        print (f"Precision: {pre}, Recall: {rec}, F1: {f1}")

except OSError as error:
    print(f"{bcolors.FAIL}Error parsing: {error}")
    sys.exit(error)
except ParseError as error:
    print(f"{bcolors.FAIL}Error parsing: {error}")
    pass
