
import validators as validator
import matlab.engine
# from nltk import pos_tag, word_tokenize
# from nltk.wsd import lesk
# from pywsd.lesk import adapted_lesk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
# from nltk.corpus import wordnet_ic
import io, json, sys
import os
os.environ['CLASSPATH'] = "jars/*"
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'Visualiser/')

import syntax_parser
import ss2fb

lemmatizer = WordNetLemmatizer() 
stemmer = PorterStemmer()
# brown = wordnet_ic.ic('ic-brown.dat')
eng = matlab.engine.start_matlab()
# test=matlab.double([0.5, 0.5, 0.0])
# print(eng.fis(4, 3, 4))# this works for calling a test function.
example_1 = "Whilst I dont like chinese food, it was safe to say that its nice"
example_1_ref =     '1000000000001000000000010000000000010000000000000100000000100000000001'
                    # '0000000000000000000000000000000000000000000000000000000000000000'
example_2 = 'This is just a test. Although it does not really matter'

# AUTOMATE THIS FIRST ie. move this inside the split function...
# leaves, tree = syntax_parser.generate_parse_tree(example_2)

PAD_CHAR = ('NULL', '')
f = open(filename + "example_out.json", "w")

current_inti_set = []
current_intj_set = []
current_ext_set = []
output_to_file = {"steps":[], "boundaries":{"computed":"", "reference":"", "windowdiff":""}, "sentence":example_2}

# TODO get the boundaries from the training docs using the correct tile and ss2fb functions. These need to parsed into the boundary objects.



def split(string, show=True): # J is the context range (j either side)
    processed_leaves = []
    # leaves, tree = syntax_parser.generate_parse_tree(string, show)
    trees = syntax_parser.generate_parse_tree(string, show)
    # print(tree)
    tree_list = []
    for t in trees:
        for i in range(len(t.leaves())):
            leaf = t.leaf_treeposition(i)
            leaf = t[leaf[:-1]]
            processed_leaves.append(leaf)
        tree_list.append(t)
    # return tree, processed_leaves
    return tree_list, processed_leaves

def compare_words(tree, word_i, word_j):
    if word_i[0] == "NULL" or word_j[0] == "NULL":
        return 0
    if word_i[0] == "None" or word_j[0] == "None":
        return 0
    sim = syntax_parser.compare_leaves(tree, word_i, word_j)
    # Words are now tuples ('They', 'PRP')
    # Use wordnet to compare the two words here.
    return sim

def internal_cohesion(tree, word_type, splice_i):
    # print(splice_i[0], splice_i[len(splice_i)-1])
    return compare_words(tree, splice_i[0], splice_i[len(splice_i)-1])

def calculate_boundary(fis, int_coh_i, int_coh_j, ext_dis):
    print(f"INT_COH_I: {int_coh_i}, INT_COH_J: {int_coh_j}, EXT_DIS: {ext_dis}")
    place_boundary = eng.fis(fis, int_coh_i, int_coh_j, ext_dis);
    return place_boundary, float(place_boundary) >= 0.6

# def tile(tree, string_arr, k, get_boundary=True): # j is the window for context.
def tile(fis, tree_list, string_arr, k, get_boundary=True): # j is the window for context.
    boundaries = ''
    # try:
    string_arr_len = len(string_arr)
    boundary_objects = []
    # print(string_arr)
  
    for tree in tree_list:
        
        # Get the boundaries from the test data.
        # if not get_boundary:
        #     test_data_boundaries = ss2fb.convert_slseg_2_fb(tree)
        # ----
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
                left_string_array = left_pad + left_string_array
            right_pad = abs(k - len(right_string_array))
            if right_pad > 0:
                right_pad = [PAD_CHAR for pad in range(right_pad)]
                right_string_array += right_pad

            left_internal_coh = internal_cohesion(tree, 'inti', left_string_array)
            # print("FUKKKK", right_string_array)
            right_internal_coh = internal_cohesion(tree, 'intj', right_string_array)
            external_dissim = compare_words(tree, left_string_array[0], right_string_array[len(right_string_array) - 1])
            
            if get_boundary:
                boundary_score, is_boundary = calculate_boundary(fis, left_internal_coh, right_internal_coh, external_dissim)
                if is_boundary:
                    boundaries += '1'
                else:
                    boundaries += '0'
                output_to_file['steps'].append({"l_int":left_internal_coh, "r_int":right_internal_coh, "e_dis":external_dissim, "bound":(boundary_score, is_boundary), "segi":left_string_array, "segj":right_string_array, "extdis":current_ext_set.copy(), "intcohi":current_inti_set.copy(), "intcohj":current_intj_set.copy()})
                current_intj_set.clear()
                current_inti_set.clear()
                current_ext_set.clear()
            else:
                boundary_objects.append((i,left_internal_coh,right_internal_coh,external_dissim))

    if get_boundary:
        validate = validator.window_diff(example_1_ref, boundaries, 3)
        output_to_file['boundaries']['computed'] = boundaries
        output_to_file['boundaries']['reference'] = example_1_ref;
        output_to_file['boundaries']['windowdiff'] = validate;

        f.write(json.dumps(output_to_file))
        return boundaries, validate
    else:
        return boundary_objects


# tree, processed_leaves = split(example_2);
# print(tile(tree, processed_leaves, 5, ))