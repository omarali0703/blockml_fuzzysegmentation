from subprocess import Popen, PIPE
import sys
import os
import json
from tkinter.tix import Y_REGION
from python_micrologic import RS3_Parser as rs3parser
from python_micrologic import SLSeg_Parser as slsegparser
from python_micrologic import RSTSentiment_Parser as sentparser
from sklearn import metrics
from xml.etree.ElementTree import ParseError
from run import start
from mlflow import log_param

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
    log_param("function", f"MICROLOGIC: {function_called}")
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
        file_counter = 0
        limit = 20 
        l_counter = 0

        binary = True # Do a bin class.
        log_param("class_type",f"{'binary' if binary else 'multiclass'}")
        log_param("sentiments_requested", f"{limit}")

        for segfile in list_path:
        
            block_counter = 0
            current_line = 0
            abs_location = os.path.join(location, segfile)
            filename = segfile.split('.')
            file_extension = filename[1]
            filename = filename[0]
            y_true = []
            y_pred = []
            print (file_extension)
            if file_extension in ['json']:

                print(f'{bcolors.OKCYAN}Loading JSON file {segfile}...{variables}')
                file_contents = open(abs_location, "r").read()
                sentiment_data = json.loads(file_contents)
                print (f"{len(sentiment_data)} Sentiments loaded.")

                sentiment_score_is_out_of = int(variables[0])
                is_rst = variables[1] = True if variables[1] == "True" else False
                is_inputted_edus = variables[2] = True if variables[2] == "True" else False
                log_param("using_rst",f"{'RST' if is_rst else 'NO RST'}")
                log_param("edus",f"{'FUZZYSEG' if is_inputted_edus else 'HILDA'}")

                print ("RST? ", is_rst, ", EXT. EDU? ", is_inputted_edus)
                files_preparsed = [] 
                sentiment_data = sentparser.randomise_sentDS(sentiment_data, limit, 'overall', sentiment_score_is_out_of, charlimit=100)
                if is_rst:
                    # Create a random array of sentiment data.
                    
                    # If we are going to input EDUs from generated/external source, in this case, FUZZYSEG.
                        # Go through sent data and produce EDUS.
                    for review in sentiment_data:
                        review['filename'] = f'input_{l_counter}.txt'

                        if is_inputted_edus:
                            # This input object imitates our FlowML inputs (Which, for text, is {filename:filecontents, ...})
                            print ("reviewing text and producing Fuzzy EDUs...")
                            from train import fseg_to_matlab
                            from preprocess_fis.block_text_tilling import split as split_func, tile as tile_func
                            try:
                                edu_data, loop = start({"input":review['reviewText']}, settings={
                                    "root":"dependencies",
                                    "training_data_path":"/phd_datasets/fuzzyseg_outputs/fis_training/generated/train_12_k3_syntax.dat",
                                    "parse_type": "syntax",
                                    "parser_output_form": "hilda"
                                }, fseg_to_matlab=fseg_to_matlab, split=split_func, tile=tile_func)
                            except:
                                l_counter += 1
                                continue
                            print ("EDUs produced for text.")
                            
                            # OPTIONAL
                            file_name = f'EDU_{l_counter}.txt'
                            cut_file_name = f'CUT_{l_counter}.txt'
                            tmp_edu_sentiment_file = open(f"dependencies/hilda-docker/{file_name}", "w")
                            tmp_cut_sentiment_file = open(f"dependencies/hilda-docker/{cut_file_name}", "w")

                            tmp_edu_sentiment_file.write(str(edu_data['edus_list']))
                            tmp_cut_sentiment_file.write(str(edu_data['cuts']))
                            review['edus'] = edu_data['edus']
                            # END OPTIONAL
                            # review['filename'] = f'input_{l_counter}.txt'
                            review['edu_filename'] = file_name
                            review['cuts_filename'] = cut_file_name

                        files_preparsed.append(review)
                        l_counter += 1
                        

                            
                    print (f"{bcolors.OKGREEN}Loading RST files into docker img...")
                    for review in files_preparsed:
                        file_name = review['filename']
                        
                        tmp_sentiment_file = open(f"dependencies/hilda-docker/{file_name}", "w")
                        tmp_sentiment_file.write(review['reviewText'])
                        print (f"{file_name} Loaded...")

                    print (f"{bcolors.OKGREEN}Building docker image... {__file__}")
                    curr_dir = os.path.dirname(__file__)
                    docker_location = curr_dir + "/dependencies/hilda-docker"
                    print (docker_location)
                    

                    p = Popen(f'docker build -t hilda {docker_location}', stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
                    outputs, err = p.communicate()
                    # print (outputs)
                    print (f"{bcolors.OKGREEN}Image built. {outputs} {err} \n\nRunning parser...")
                else:
                    files_preparsed = sentiment_data
                
                l_counter = 0
                pass # TODO pass RST files into docker img and build. Once built, return list of files that are inputs to HILDA. Run HILDA on these files and return RST trees.
                for review in files_preparsed:
                    review_sentence = review['reviewText']
                    if is_inputted_edus:
                        review_edus = review['edus']
                    if (binary):
                        print (review['overall'])
                        review_reference_score = 1 if int(float(review['overall'])) > 3 else 0
                    else:
                        review_reference_score = int(float(review['overall']))

                    rst_tree = None
                    print (f"{bcolors.OKGREEN}Parsing input_{l_counter}.txt...")

                    try:
                        if is_rst:
                            w=[]
                            # we need to open a tmp file so we can input its location into the HILDA wrapper. 
                            # This is a work around as i don't fancy updating the HILDa wrapper code and i'm lazy.
                            print (f"{bcolors.OKBLUE}Generating RST trees...")
                            if is_inputted_edus:
                                print (review)
                                rst_tree = sentparser.get_rst_tree(review['filename'], review['edu_filename'], review['cuts_filename'])
                                print (f"{bcolors.OKBLUE}FINISHED Generating RST trees...")
                            else:
                                rst_tree = sentparser.get_rst_tree(review['filename'], )
                                print (f"{bcolors.OKBLUE}FINISHED Generating RST trees...")
                            
                            chosen_rst_weights = sentparser.LIGHT

                            log_param("chosen_rst_weights", f"{chosen_rst_weights}")
                            sentparser.weight_RST(weights=w, tup_obj=rst_tree, weighting_scheme=chosen_rst_weights)
                            # print (w)
                            computed = 0
                            tokens = 1
                            for weighted_edu in w:
                                weight = weighted_edu[1]
                                # TODO Make sure this is weighting properly

                                text = weighted_edu[0]
                                sent_score = sentparser.parse_sentence_LESK(text, 1, sentiment_score_is_out_of if not binary else 1, weight, binary)
                                # print (weight,sent_score )
                                if sent_score > 0:
                                    tokens += 1
                                computed +=sent_score
                                # computed *= weight
                            output = computed/tokens
                            
                         
                            if binary:
                                print ("BEFORE MAP: ", output)
                                output = sentparser.map(output, -100, 100, 0, 1)
                                print ("AFTER MAP: ", output)

                                # output = 1 if sentparser.map(computed, -1, 1, 1, sentiment_score_is_out_of) > (sentiment_score_is_out_of//2) else 0
                                # output = sentparser.map(computed/tokens, 0, sentiment_score_is_out_of, 0, 1)
                                if output > 0.5:
                                    output = 1
                                else:
                                    output = 0
                            else:
                                mid = 50
                                sc = mid + output
                                print ("BEFORE MAP & MID: ", sc)
                                output = sentparser.map(sc, 0, 100, 0, sentiment_score_is_out_of)
                                print ("AFTER MAP: ", output)

                                output = int(round(output))
                            print("COMP",computed, "COMPO", output, "TOKENS", tokens, computed/tokens)

                            # print ("SENTIMENT? ", output, computed)
                            l_counter += 1

                        else:
                            print (f"{bcolors.OKGREEN}Finished parsing...")
                            
                            computed = sentparser.parse_sentence_LESK(review_sentence, 1, sentiment_score_is_out_of if not binary else 1, 1, True)
                            print ("COMPUTED", computed)
                            if computed == None:
                                continue
                            l_counter += 1
                            # output = 1 if computed > 0 else 0

                            if binary:
                                output = sentparser.map(computed, -100, 100, 0, 1)
                                if output > 0.5:
                                    output = 1
                                else:
                                    output = 0
                            else:
                                mid = 50
                                sc = mid + computed
                                output = sentparser.map(sc, 0, 100, 0, sentiment_score_is_out_of)
                                output = int(round(output))
                                print ("NORMALISED: ", output)

                        y_true.append(review_reference_score)
                        y_pred.append(output)
                        print ("NEW LISTs: ", y_true, y_pred)
                    except Exception as e:
                        print (f"{bcolors.FAIL}Failed to generate RST tree. {e}")
                        l_counter += 1
                        continue
                            
                 
            file_counter += 1
            log_param("sentiments_processed", f"{l_counter}")
            log_param("y_true", f"{y_true}")
            log_param("y_pred", f"{y_pred}")
            cf = metrics.confusion_matrix(y_true=y_true, y_pred=y_pred)
            cp = metrics.classification_report(y_true=y_true, y_pred=y_pred, digits=3, output_dict=True)
            cp_macro = cp['macro avg']
            cp_accuracy = cp['accuracy']
            cp_mac_pre = cp_macro['precision']
            cp_mac_rec = cp_macro['recall']
            cp_mac_f1s = cp_macro['f1-score']
            log_param("cp_mac_pre", f"{cp_mac_pre}")
            log_param("cp_mac_rec", f"{cp_mac_rec}")
            log_param("cp_mac_f1s", f"{cp_mac_f1s}")
            log_param("cp_accuracy", f"{cp_accuracy}")
            log_param("confusion_matrix", f"{cf}")

            print (y_true, y_pred)
            print(cf)
            print(cp)


except OSError as error:
    print(f"{bcolors.FAIL}Error parsing: {error}")
    sys.exit(error)
except ParseError as error:
    print(f"{bcolors.FAIL}Error parsing: {error}")
    pass
