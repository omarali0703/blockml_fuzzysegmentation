
from . import block_syntax_parser as syntax_parser
from . import validators as validator
import matlab.engine
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import io
import json
import sys
import os
os.environ['CLASSPATH'] = "../../dependencies/jars/*"
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../visualiser/')
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
eng = matlab.engine.start_matlab()
example_1 = "Whilst I dont like chinese food, it was safe to say that its nice"
example_1_ref = '1000000000001000000000010000000000010000000000000100000000100000000001'
example_2 = 'This is just a test. Although it does not really matter'
PAD_CHAR = ('NULL', '')
f = open(filename + "fuzzy_seg_tilling_output.json", "w")
current_inti_set = []
current_intj_set = []
current_ext_set = []
output_to_file = {"steps": [], "boundaries": {"computed": "",
                                              "reference": "", "windowdiff": ""}, "sentence": example_2}
print('BLOCK TEXT TILLING LOADED')


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


def split(string, show=True):  # J is the context range (j either side)
    print(f'{bcolors.OKCYAN}Begin splitting ...')
    processed_leaves = []
    trees = syntax_parser.generate_parse_tree(string, show)
    tree_list = []
    for t in trees:
        for i in range(len(t.leaves())):
            leaf = t.leaf_treeposition(i)
            leaf = t[leaf[:-1]]
            processed_leaves.append(leaf)
        tree_list.append(t)
    return tree_list, processed_leaves


def compare_words(tree, word_i, word_j):
    if word_i[0] == "NULL" or word_j[0] == "NULL":
        return 0
    if word_i[0] == "None" or word_j[0] == "None":
        return 0
    sim = syntax_parser.compare_leaves(tree, word_i, word_j)
    return sim

# Comparewords (Uses CompareLeavesAVG method) samples all leaves not just first and last.


def compare_words_AVG(tree, words):
    for word in words:
        if word[0] == "NULL" or word[0] == "None":
            print("is null")

            return 0

    sim = syntax_parser.compare_leaves_AVG(tree, words)
    # Words are now tuples ('They', 'PRP')
    # Use wordnet to compare the two words here.
    return sim


def internal_cohesion_AVG(tree, word_type, words):
    # print(splice_i[0], splice_i[len(splice_i)-1])
    return compare_words_AVG(tree, words)


def internal_cohesion(tree, word_type, splice_i):
    return compare_words(tree, splice_i[0], splice_i[len(splice_i)-1])


# This needs to take the generated FIS as an input.
def calculate_boundary(fis, int_coh_i, int_coh_j, ext_dis):
    print(
        f"INT_COH_I: {int_coh_i}, INT_COH_J: {int_coh_j}, EXT_DIS: {ext_dis}")
    place_boundary = eng.fis(fis, int_coh_i, int_coh_j, ext_dis)
    return place_boundary, float(place_boundary) >= 0.6


# True boundaries are a bin rep of the input data.
# If provided then these are used if get_boundary is true.
def tile(fis, tree_list, string_arr, k, get_boundary=True, true_boundaries=None):
    print(f'{bcolors.OKCYAN}Begin tilling ...')

    boundaries = ''
    print(len(string_arr))
    string_arr_len = len(string_arr)
    boundary_objects = []
    for tree in tree_list:
        for i in range(len(string_arr) + 1):
            left_splice = i - k
            right_splice = i + k
            if left_splice < 0:
                left_splice = 0
            if right_splice > string_arr_len:
                right_splice = string_arr_len
            left_string_array = string_arr[left_splice:i]
            right_string_array = string_arr[i:right_splice]
            left_pad = abs(k - len(left_string_array))
            if left_pad > 0:
                left_pad = [PAD_CHAR for pad in range(left_pad)]
                # print("TEST", left_string_array, left_pad,
                #   type(left_string_array), type(left_pad))
                left_string_array = left_pad + left_string_array
                print('2')
            right_pad = abs(k - len(right_string_array))
            if right_pad > 0:
                right_pad = [PAD_CHAR for pad in range(right_pad)]
                right_string_array += right_pad

            # left_internal_coh = internal_cohesion(tree, 'inti', left_string_array)
            # right_internal_coh = internal_cohesion(tree, 'intj', right_string_array)
            # external_dissim = compare_words(tree, left_string_array[0], right_string_array[len(right_string_array) - 1])
            #
            #                  ||||||||
            # AVG method below VVVVVVVV
            left_internal_coh = internal_cohesion_AVG(
                tree, 'inti', left_string_array)
            right_internal_coh = internal_cohesion_AVG(
                tree, 'intj', right_string_array)
           
            (print("calc exd", left_string_array, right_string_array,
                   type(left_string_array), type(right_string_array)))
            external_dissim = compare_words_AVG(
                tree, left_string_array + right_string_array)

            if get_boundary:
                if not true_boundaries:
                    boundary_score, is_boundary = calculate_boundary(
                        fis, left_internal_coh, right_internal_coh, external_dissim)
                    if is_boundary:
                        boundaries += '1'
                    else:
                        boundaries += '0'

                        output_to_file['steps'].append({"l_int": left_internal_coh, "r_int": right_internal_coh, "e_dis": external_dissim, "bound": (
                            boundary_score, is_boundary), "segi": left_string_array, "segj": right_string_array, "extdis": current_ext_set.copy(), "intcohi": current_inti_set.copy(), "intcohj": current_intj_set.copy()})
                else:
                    # Get the boundaries from a bin rep of the training data.
                    print(i, len(true_boundaries))
                    boundaries = true_boundaries[i]
                    output_to_file['steps'].append({"l_int": left_internal_coh, "r_int": right_internal_coh, "e_dis": external_dissim, "bound": (
                        boundaries), "segi": left_string_array, "segj": right_string_array, "extdis": current_ext_set.copy(), "intcohi": current_inti_set.copy(), "intcohj": current_intj_set.copy()})

                current_intj_set.clear()
                current_inti_set.clear()
                current_ext_set.clear()
            else:
                boundary_objects.append(
                    (i, left_internal_coh, right_internal_coh, external_dissim))

    print(f'{bcolors.OKGREEN}Finished tilling process..... (So close :D!)')

    if get_boundary:
        validate = validator.window_diff(example_1_ref, boundaries, 3)
        output_to_file['boundaries']['computed'] = boundaries
        output_to_file['boundaries']['reference'] = example_1_ref
        output_to_file['boundaries']['windowdiff'] = validate
        f.write(json.dumps(output_to_file))
        return boundaries, validate, output_to_file
    else:
        return boundary_objects


# tree, processed_leaves = split(example_2);
# print(tile(tree, processed_leaves, 5, ))
