import matlab.engine
import matlab
import os
from os import listdir
from os.path import isfile, join
from mlflow_projects.fuzzy_segmentation import train

from mlflow_projects.fuzzy_segmentation.train import fseg_to_matlab
from ..preprocess_fis.block_text_tilling import *
from ..python_micrologic.RS3_Parser import *
INPUT_FLOW = ""
OUTPUT_FLOW = "results"
from progress.bar import Bar


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


eng = matlab.engine.start_matlab()


def fuzzy_segment(fuzzy_system, file_str, settings):
    with Bar('Segmenting input source ...', max=7) as bar:
        tree, processed_leaves = split(file_str, show=False, parse_type=settings['parse_type'])
        bar.next()
        boundaries, tiled_data = tile(eng, fuzzy_system, tree, processed_leaves, 3, get_boundary=True, true_boundaries=None)
        bar.next()
        print (boundaries)
        is_hilda = settings['hilda'] == True
        is_spade = settings['spade'] == True
        is_array = not is_hilda and not is_spade
        return_string = [] if is_array else ''
        SPLIT_TOKEN = '~[SPLIT]~'
        file_str = file_str.replace('(', f"({SPLIT_TOKEN}")
        file_str = file_str.replace(')', f"{SPLIT_TOKEN})")
        file_str = file_str.replace('£', f"£{SPLIT_TOKEN}")
        file_str = file_str.replace('%', f"{SPLIT_TOKEN}%")
        file_str = file_str.replace('$', f"${SPLIT_TOKEN}")
        file_str = file_str.replace(',', f"{SPLIT_TOKEN},")
        file_str = file_str.replace(' ', f"{SPLIT_TOKEN}")
        file_str = file_str.replace('-', f"{SPLIT_TOKEN}")
        file_str = file_str.replace('.', f"{SPLIT_TOKEN}.")
        file_str_arr = file_str.split(SPLIT_TOKEN)
        
        
        print (file_str_arr, len(file_str_arr), len(boundaries))
        index = 0
        return_string = "<edu>" if is_hilda else "<edu>" # TODO make sure to account for SPADE formats here.
        for boundary_token in boundaries[1:]:
            if is_hilda:                
                if int(boundary_token) == 1:
                    return_string += f"{file_str_arr[index]} </edu>"
                    return_string += "<edu>" if is_hilda else "<edu>" # TODO make sure to account for SPADE formats here.
                else:
                    return_string += f"{file_str_arr[index]} "
                # HILDA_form = f"<edu>{segment}</edu>\n"
                # return_string += HILDA_form
            # elif is_array:
            #     return_string.append(segment)

            index += 1
        return return_string + "</edu>"

f_newline='\n'
def start(input_data=None, settings={}, loop_breaker=None):
    print(f"""\n\n{bcolors.OKGREEN + bcolors.BOLD}Welcome to FuzzySeg.

This project is currently in developement.

FuzzySeg is a fuzzy-logic based segmentation model designed and implemented
by Omar Ali at the University of Portsmouth (omar.ali1@port.ac.uk).
If you have any questions or issues with the implementation please feel
free to email me.

For more information and citation on the exact details of the model please use:


Text Segmentation Using Light Syntax Parsing and Fuzzy Systems
Omar Ali, Alexander Gegov, Ella Haig and Rinat Khusainov
International Conference on Intelligent and Fuzzy Systems
pages 36 - 43
2021
Springer

Beginning to process the inputs provided\n
{f_newline.join([f'{i}: {settings[i]}' for i in settings])}\n...
""")
    eng.cd('/Users/omarali/Documents/mlflow_source/mlflow_projects/fuzzy_segmentation/train')
    training_data = open(settings['root'] + settings['training_data_path']).read()
    training_data = training_data.split('\n')
    if training_data[-1] == '':
        training_data = training_data[:-1]

    # print (training_data)
    training_data = fseg_to_matlab(training_data)
    fuzzy_system = eng.train(training_data, True)
    output_dir = settings['root'] + settings['output_data_path']
    parse_type = settings['parse_type']
    parser_output_form = settings['parser_output_form']
    out_is_dir = os.path.isdir(output_dir)
    
    if not out_is_dir:
        print(f"{bcolors.WARNING}{output_dir} is not a directory.")
    
    if input_data == None:
        print(f"{bcolors.WARNING}Please specify a correct input data source to segment.")

    print ('Begin segmenting...')
    for data in input_data:
        output_edus = fuzzy_segment(fuzzy_system, input_data[data], {
                'parse_type':parse_type,
                'hilda':parser_output_form == "hilda",
                'spade':parser_output_form == "spade"
            }
        )
        print (output_edus)
    return json.dumps({"edus":output_edus}), None