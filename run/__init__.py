from curses import curs_set
import matlab.engine
import matlab
import os
import json
from os import listdir

from os.path import isfile, join
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


def fuzzy_segment(fuzzy_system, file_str, settings, split=None, tile=None):
    if split == None or tile==None:
        from ..preprocess_fis.block_text_tilling import tile as _tile, split as _split

    with Bar('Segmenting input source ...', max=7) as bar:
        
        if split == None or tile==None:
            tree, processed_leaves = _split(file_str, show=False, parse_type=settings['parse_type'])
        else:
            tree, processed_leaves = split(file_str, show=False, parse_type=settings['parse_type'])

        bar.next()
        if split == None or tile==None:
            boundaries, tiled_data = _tile(eng, fuzzy_system, tree, processed_leaves, 3, get_boundary=True, true_boundaries=None)
        else:
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
        file_str = file_str.replace('!', f"{SPLIT_TOKEN}!")
        file_str = file_str.replace('%', f"{SPLIT_TOKEN}%")
        file_str = file_str.replace('$', f"${SPLIT_TOKEN}")
        file_str = file_str.replace(',', f"{SPLIT_TOKEN},")
        file_str = file_str.replace(' ', f"{SPLIT_TOKEN}")
        file_str = file_str.replace('-', f"{SPLIT_TOKEN}")
        file_str = file_str.replace('.', f"{SPLIT_TOKEN}.")
        file_str = file_str.replace('`', f"{SPLIT_TOKEN}`")
        file_str = file_str.replace("'", f"{SPLIT_TOKEN}'")
        file_str_arr = file_str.split(SPLIT_TOKEN)
        
        
        print (file_str_arr, len(file_str_arr), len(boundaries))
        index = 1

        # HILDA STUFF
        edu_list = []
        cuts_list = []
        
        '''
        HILDA CUTS
        [[(0, 11), (11, 21)], [(0, 9)], [(0, 9), (9, 14), (14, 23), (23, 29)], [(0, 7), (7, 11), (11, 26), (26, 34)], [(0, 7), (7, 13)], [(0, 13), (13, 29), (29, 37), (37, 48)], [(0, 23)], [(0, 3), (3, 11)], [(0, 13)], [(0, 11), (11, 22)], [(0, 2), (2, 5)], [(0, 7), (7, 36)], [(0, 4), (4, 18)], [(0, 26), (26, 36)], [(0, 8), (8, 16), (16, 19), (19, 24), (24, 26), (26, 34)]]
        
        HILDA EDUS
        [['henryk', 'szeryng', '(', '22', 'september', '1918', '-', '8', 'march', '1988', ')'], ['was', 'a', 'violin', 'virtuoso', 'of', 'polish', 'and', 'jewish', 'heritage', '.'], ['he', 'was', 'born', 'in', 'zelazowa', 'wola', ',', 'poland', '.'], ['henryk', 'started', 'piano', 'and', 'harmony', 'training', 'with', 'his', 'mother'], ['when', 'he', 'was', '5', ','], ['and', 'at', 'age', '7', 'turned', 'to', 'the', 'violin', ','], ['receiving', 'instruction', 'from', 'maurice', 'frenkel', '.'], ['after', 'studies', 'with', 'carl', 'flesch', 'in', 'berlin'], ['(', '1929-32', ')', ','], ['he', 'went', 'to', 'paris', 'to', 'continue', 'his', 'training', 'with', 'jacques', 'thibaud', 'at', 'the', 'conservatory', ','], ['graduating', 'with', 'a', 'premier', 'prix', 'in', '1937', '.'], ['he', 'made', 'his', 'solo', 'debut', 'in', '1933'], ['playing', 'the', 'brahms', 'violin', 'concerto', '.'], ['from', '1933', 'to', '1939', 'he', 'studied', 'composition', 'in', 'paris', 'with', 'nadia', 'boulanger', ','], ['and', 'during', 'world', 'war', 'ii', 'he', 'worked', 'as', 'an', 'interpreter', 'for', 'the', 'polish', 'government', 'in', 'exile'], ['(', 'szeryng', 'was', 'fluent', 'in', 'seven', 'languages', ')'], ['and', 'gave', 'concerts', 'for', 'allied', 'troops', 'all', 'over', 'the', 'world', '.'], ['during', 'one', 'of', 'these', 'concerts', 'in', 'mexico', 'city', 'he', 'received', 'an', 'offer', 'to', 'take', 'over', 'the', 'string', 'department', 'of', 'the', 'university', 'there', '.'], ['in', '1946', ','], ['he', 'became', 'a', 'naturalized', 'citizen', 'of', 'mexico', '.'], ['szeryng', 'subsequently', 'focused', 'on', 'teaching', 'before', 'resuming', 'his', 'concert', 'career', 'in', '1954', '.'], ['his', 'debut', 'in', 'new', 'york', 'city', 'brought', 'him', 'great', 'acclaim', ','], ['and', 'he', 'toured', 'widely', 'for', 'the', 'rest', 'of', 'his', 'life', '.'], ['he', 'died'], ['in', 'kassel', '.'], ['szeryng', 'made', 'a', 'number', 'of', 'recordings', ','], ['including', 'two', 'of', 'the', 'complete', 'sonatas', 'and', 'partitas', 'for', 'violin', 'by', 'johann', 'sebastian', 'bach', ',', 'and', 'several', 'of', 'sonatas', 'of', 'beethoven', 'and', 'brahms', 'with', 'the', 'pianist', 'arthur', 'rubinstein', '.'], ['he', 'also', 'composed', ';'], ['his', 'works', 'include', 'a', 'number', 'of', 'violin', 'concertos', 'and', 'pieces', 'of', 'chamber', 'music', '.'], ['he', 'owned', 'the', 'del', 'gesu', '``', 'le', 'duc', "''", ',', 'the', 'stradivarius', '``', 'king', 'david', "''", 'as', 'well', 'as', 'the', 'messiah', 'strad', 'copy', 'by', 'jean-baptiste', 'vuillaume'], ['which', 'he', 'gave', 'to', 'prince', 'rainier', 'iii', 'of', 'monaco', '.'], ['the', '``', 'le', 'duc', "''", 'was', 'the', 'instrument'], ['on', 'which', 'he', 'performed', 'and', 'recorded', 'mostly', ','], ['while', 'the', 'latter'], ['(', '``', 'king', 'david', "''"], ['strad', ')'], ['was', 'donated', 'to', 'the', 'state', 'of', 'israel', '.']]
        
        '''

        return_string = "<edu>" if is_hilda else "<edu>" # TODO make sure to account for SPADE formats here.
        current_edu = []
        current_edu_cut = []
        cut_start = 0
        cut_end = 0
        cut_tuple = ()
        for boundary_token in boundaries[1:]:
            
            if is_hilda:                
                if int(boundary_token) == 1:
                    current_edu.append(file_str_arr[index])
                    edu_list.append(current_edu)
                    current_edu = []
                    cut_tuple = (cut_start, cut_end)
                    cut_start = cut_end
                    current_edu_cut.append(cut_tuple)

                    return_string += f"{file_str_arr[index]} </edu>\n"
                    print(file_str_arr[index])
                    if file_str_arr[index] == '.':
                        print ('fullstop')
                        cut_start = 0
                        cut_end = 0
                        cuts_list.append(current_edu_cut)
                        current_edu_cut = []
                    return_string += "<edu>" if is_hilda else "<edu>" # TODO make sure to account for SPADE formats here.
                else:
                    current_edu.append(file_str_arr[index])
                    cut_end += 1
                    return_string += f"{file_str_arr[index]} "
                # HILDA_form = f"<edu>{segment}</edu>\n"
                # return_string += HILDA_form
            # elif is_array:
            #     return_string.append(segment)

            index += 1
        print ("HILDA EDUS & CUTS:", edu_list, cuts_list)
        return return_string + "</edu>\n", edu_list, cuts_list

f_newline='\n'
def start(input_data=None, settings={}, loop_breaker=None, fseg_to_matlab=None, split=None, tile=None):
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
    if fseg_to_matlab:
        training_data = fseg_to_matlab(training_data)
    else:
        from mlflow_projects.fuzzy_segmentation.train import fseg_to_matlab as fs2matlab
        training_data = fs2matlab(training_data)

    fuzzy_system = eng.train(training_data, True)
    if 'output_data_path' in settings:
        output_dir = settings['root'] + settings['output_data_path']
        out_is_dir = os.path.isdir(output_dir)
        if not out_is_dir:
            print(f"{bcolors.WARNING}{output_dir} is not a directory.")
    
    parse_type = settings['parse_type']
    parser_output_form = settings['parser_output_form']
    
   
    if input_data == None:
        print(f"{bcolors.WARNING}Please specify a correct input data source to segment.")

    print ('Begin segmenting...')
    for data in input_data:
        output_edus, edus_list, output_cuts = fuzzy_segment(fuzzy_system, input_data[data], {
                'parse_type':parse_type,
                'hilda':parser_output_form == "hilda",
                'spade':parser_output_form == "spade"
            },
            split=split,
            tile=tile
        )
        print (output_edus)
    return {"edus":output_edus, "edus_list":edus_list, "cuts":output_cuts}, None