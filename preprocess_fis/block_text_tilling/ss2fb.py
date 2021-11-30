import re
import block_text_tilling as tt
import os
from nltk.tokenize import word_tokenize

segEx = '''<T>
<P>
</P>
<P>
<S>
<C>Whilst/NNP i/PRP do/AUX believe/VB that/DT segmentation/NN using/VBG syntax/NN is/AUX promising/VBG ,/, </C>
<C>I/PRP do/AUX find/VB that/IN ocassionally/RB there/EX are/AUX some/DT difficulties/NNS ./. </C>
</S>
<S>
<C>Typically/RB you/PRP may/MD want/VB to/TO segment/NN using/VBG keywords/NNS or/CC cues/NNS ,/, </C>
<C>however/RB ,/, a/DT unique/JJ set/NN of/IN cue/NN phrases/NNS will/MD need/AUX to/TO be/AUX produces/VBZ </C>
<C>in/IN order/NN to/TO account/VB for/IN all/DT applications/NNS ./. </C>
</S>
<S>
<C>This/DT may/MD prove/VB to/TO be/AUX difficult/JJ and/CC time/NN consuming/NN ./. </C>
</S>
</P>
</T>
'''

# test

def new_convert_slseg_2_fb(slseg, indexed_list=False):
    slseg = re.sub(r'-', '', slseg)
    slseg = re.sub(r'["]*', '', slseg)
    slseg = re.sub(r'[\'`]*', '', slseg)
    slseg = re.sub(r'<[/]*[A-Z]+>', '', slseg)
    slseg = slseg.replace(':', '')
    slseg = re.sub(r'/[a-zA-Z0-9!@£$%^&*.,`]*', '', slseg)
    word_count = 0
    # slseg = re.sub(r'[/]*[,.?:;]', '', slseg)

    slseg = slseg.split('\n')
    segmentation = '1'
    my_words = ''
    # print(slseg)
    for sentence in slseg:
        if sentence == '':
            continue
        parsed_sentence = word_tokenize(sentence)
        sentence_length = len(parsed_sentence)
        sentence_length_index = 1
        for word in parsed_sentence:
            my_words += word + ' || '

            word_count += 1
            if sentence_length_index == sentence_length:
                segmentation += '1'
            else:
                segmentation += '0'
            
            sentence_length_index += 1
    print("SLSEG", my_words)
    return segmentation


def convert_slseg_2_fb(slseg, indexed_list=False):
    slseg = re.sub(r'-', '', slseg)
    slseg = re.sub(r'[/]*[a-zA-Z0-9]', '', slseg)

    slseg = re.sub(r'[a-zA-Z0-9!@£$%^&*.,]*/[A-Z0-9&$£!@.,]* ', '0', slseg)
    
    print('first pass', slseg)
    slseg = re.sub(r'[/]*[,.?:;]', '', slseg)
    print('second pass', slseg)
    slseg = re.sub(r'(<[/]*[A-Z]+>\n)+(<[/]*[A-Z]+>)+', "1", slseg)
    slseg = re.sub(r'(<[/]*[A-Z]+>)', "1", slseg)
    print('third pass', slseg)

    slseg = re.sub(r' ', '', slseg)
    slseg = re.sub(r'Â', '', slseg)
    slseg = re.sub(r'-LRB-', '', slseg)
    slseg = re.sub(r'-RRB-', '', slseg) # This may cause an issue.
    slseg = re.sub(r'``', '', slseg)
    slseg = re.sub(r'/', '', slseg)
    slseg = re.sub(r'\'', '', slseg)
    slseg = re.sub(r'\n', '', slseg)
    print('fourth pass(trim spaces and extra chars)', slseg)

    if indexed_list:
        index = 0
        indexes = []
        for seg in slseg:
            if seg == 1:
                indexed.append(index)
            index += 1
        return slseg, indexed_list

    return slseg

# print(convert_slseg_2_fb(segEx))

#Converting segbot's output to a binary format for the validators.
def convert_segbot_2_bin(segbot_input): 
    segmentation = '1'
    segbot_input = segbot_input.replace(r'-', '')
    segbot_input = segbot_input.replace(r'``', '')
    segbot_input = segbot_input.replace(r'\'', '')
    # segbot_input = re.sub(r'[a-zA-Z0-9!@£$%^&*.,`]+', '', segbot_input)

    # segbot_input = re.sub(r'[`]+', 'FUCK', segbot_input)
    segbot_input = segbot_input.split('\n')

    word_count = 0
    my_words = ''
    for sentence in segbot_input:
        if sentence == '':
            continue

        parsed_sentence = word_tokenize(sentence)
        sentence_length = len(parsed_sentence)
        sentence_length_index = 1
        for word in parsed_sentence:
            if word == '``' or word == '':
                continue
            word_count += 1
            my_words += word + ' || '
            if sentence_length_index == sentence_length:
                segmentation += '1'
            else:
                segmentation += '0'
            
            sentence_length_index += 1
    print("SEGBOT", my_words)
    return segmentation

def obtain_boundary_objects(fis, text, segs, slseg=False, k=3, get_boundary=False):
    temp_seg_ex = text

    if (slseg):
        text = re.sub(r'/[.,?\'"`A-Z]*', '', text)
        text = re.sub(r' [.]', '.', text)
        text = re.sub(r' [,]', ',', text)
        text = re.sub(r' [;]', ';', text)
        text = re.sub(r' [?]', '?', text)
        text = re.sub(r' [!]', '!', text)
        text = re.sub(r'(<[/]*[A-Z]*>)', '', text)
        text = re.sub(r'\n', '', text)
    # print(text)

    # tree, processed_leaves = tt.split(text, show=False)
    tree_list, processed_leaves = tt.split(text, show=False)
    # print(tree_list)
    # We then need to use the split function (text_tilling version) on 'text' instead of .split() and tile using that instead.
    
    boundary_raw, indexed_list = convert_slseg_2_fb(temp_seg_ex, indexed_list=True)
    
    # boundary_objects = tt.tile(tree, processed_leaves, k, get_boundary=False, )
    
    # TODO HERE IS WHERE THE ISSUE IS WITH THE 343 instances as opposed to 49/50
    boundary_objects = tt.tile(fis,
        tree_list, processed_leaves, k, get_boundary=get_boundary, )
    print(len(boundary_objects))
    for b in boundary_objects:
        b = b[:1]+(b, )+b[1:]
    # print(boundary_objects)
    return boundary_objects, boundary_raw, text



def write_as_dat(variables, data, file, included_bounds=None):
    f = open(file, "w")

    parsed_variables = ''
    parsed_data = '['
    included_bounds_index=0
    bound_object_to_write = 'NULL'
    print('FIRST CHECK LEN ', len(included_bounds))
    print('LEN CHECK 1A ', data, len(data))

    for data_point in data:
        if included_bounds:
            bound_object_to_write=included_bounds[included_bounds_index]
            
        parsed_data += f'{bound_object_to_write},{data_point[1]},{data_point[2]},{data_point[3]}\n'
        print('SEC CHECK LEN ', included_bounds_index)
    
        included_bounds_index+=1
    
    parsed_data += ']'
    f.write(parsed_data)
    f.close()


def write_as_arff(variables, data, file):
    f = open(file, "w")

    parsed_variables = ''
    parsed_data = ''

    for var in variables:
        parsed_variables += f'@ATTRIBUTE {var}\n'

    for data_point in data:
        print(data_point)
        parsed_data += f'{data_point[0]},{"boundary" if data_point[1] == "1" else "no_boundary"},{data_point[2]},{data_point[3]}\n'

    structured_file = f'@RELATION fuzzy_seg_training_data\n{parsed_variables}\n@DATA\n{parsed_data}'
    f.write(structured_file)
    f.close()


# boundary_objects = obtain_boundary_objects(segEx, None, slseg=True, k=3)
# write_as_arff(['index NUMERIC', 'bound_no_bound {boundary,no_boundary}', 'inti NUMERIC',
#                'intj NUMERIC', 'ext NUMERIC'], boundary_objects, 'classify_boundaries.arff')
