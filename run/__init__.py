import matlab.engine
import matlab
import os
from ..preprocess_fis.block_text_tilling import *
from ..python_micrologic.RS3_Parser import *
INPUT_FLOW = ""
OUTPUT_FLOW = "results"


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


# eng = matlab.engine.start_matlab()


def fuzzy_segment(fuzzy_system, *settings):
    edus = eng.run_and_get_edus(fuzzy_system, settings['training_data_path'])
    is_hilda = 'hilda' in settings and settings['hilda'] == True
    # Will default to true of hilda isn't present...
    is_array = not is_hilda
    # TODO need a SPADE form? other RST parsers?
    return_string = "" if is_hilda else []  # default to array

    for segment in edus:
        if is_hilda:
            HILDA_form = f"<edu>{segment}</edu>\n"
            return_string += HILDA_form
        elif is_array:
            return_string.append(segment)

    return return_string

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
Ali, Omar and Gegov, Alexander and Haig, Ella and Khusainov, Rinat
International Conference on Intelligent and Fuzzy Systems
pages 36 - 43
2021
Springer

Beginning to process the inputs provided\n
{f_newline.join([f'{i}: {settings[i]}' for i in settings])}\n...
""")
 
    # fuzzy_system = eng.train(settings['training_data_path'], False)
    output_dir = settings['output_data_path']
    parse_type = settings['parse_type']
    is_dir = os.path.isdir(output_dir)
    
    if not is_dir:
        return f"{bcolors.WARNING}{output_dir} is not a directory."
    
    RS3_generate_fis_training_data(tile, split, abs_location, variables[0], str(number_of_docs_to_parse_index), int(variables[2]), parse_type=variables[3])

    # edus = fuzzy_segment(fuzzy_system, *settings)
