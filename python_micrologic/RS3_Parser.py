import io
from os import write, path, listdir
import xml.etree.ElementTree as ET
# from ..preprocess_fis.block_text_tilling import tile, split
# from ..preprocess_fis.block_text_tilling import *
# Retrieve the segmentations from the RST file.
# if Bin, return the FuzzySeg version (binary), otherwise return a parsed list
# Output_location is not including the file name itself. This is taken from the location.
# The location variable includes the file name we are parsing.


def parse_rs3(location, bin=True, output_location=None):
    # if 'vavau' not in location:
    #     return
    try:
        rst = ET.parse(location)
        root = rst.getroot()
        segments = []
        print(output_location)
        for child in root:
            child_tag = child.tag
            child_attr = child.attrib
            # Enforce str type.
            if bin:
                segments = '1'
            if child_tag == 'body':
                # parse the segments in this section
                for segment_tag in child:
                    segment_text = segment_tag.text
                    if not bin:
                        segments.append(segment_text)
                    elif segment_text:
                        segments += '0'*(len(segment_text.strip().split(' '))-1)
                        # segments += '0'*len(segment_text.split(' '))
                        segments += '1'
            elif child_tag == 'head':
                # TODO Parse the RST structure here?
                # TODO RST Main structure is stored here. Links and deps are determined here.
                pass
        if output_location:
            print('saving segments...')
            file_name = location.split('/')
            print(file_name)
            file_name = file_name[len(file_name)-1]
            output_location = path.join(output_location, file_name)
            output_location = open(output_location, 'w')
            output_location.write(segments)
            output_location.close()
            # print(f'segments saved {file_name}')

        return segments
    except OSError as error:
        print (error)

# Write_to_file is the location of the folder.
# This should not include the filename at the end.
# This is generated using the location var.


def get_original_text(location=None, write_to_file=None, called_from_micrologic=False):
    print('Begin getting original text....')
    # if called_from_micrologic:
        # location = path.join('../', location)
    # TODO Add same IF for write_to_file location -> May not be ness. for now.
    print (location)
    
    try:
        rst = ET.parse(location)
        print(rst)
        root = rst.getroot()
        filename = location.split('/')
        filename = filename[len(filename)-1]
        filename = filename.split('.')[0]
        filename += '_raw_text.txt'
        original_text = ''
        for child in root:
            child_tag = child.tag
            child_attr = child.attrib
            if child_tag != 'body':
                continue
            # parse the segments in this section
            for segment_tag in child:
                segment_text = segment_tag.text
                if segment_text != None:
                    original_text += (" "+segment_text)

        original_text = original_text.replace('  ', ' ')
        original_text = original_text.replace(' .', '. ')
        original_text = original_text.replace(' , ', ', ')
        original_text = original_text.replace(' ,', ', ')
        original_text = original_text.replace(' :', ': ')
        original_text = original_text.replace(' \ ', ' ')
        original_text = original_text.replace(' \'s', '\'')
        original_text = original_text.replace(' \'', '\'')

        if write_to_file:
            write_to_file = path.join(write_to_file, filename)
            output_file = open(write_to_file, 'w')
            output_file.write(str(original_text).strip())
            output_file.close()
            print(write_to_file)
            return write_to_file  # Return the location
        return original_text
    except OSError as error:
        print(error)
    

# This code parses the GUM RST bits and produces the raw versions
# (To be segmented by SLSeg and SEGBot?) and produces the BIN outs from the already GUM-parsed text (taken from the GUM-RST outs)

# rst_directory = '../dependencies/phd_datasets/gum_dataset/rst/rstweb/'
# output_location_raw = '../dependencies/phd_datasets/gum_outputs/original_gum_text/'
# output_location_bin = '../dependencies/phd_datasets/gum_outputs/original_gum_text_bin/'
# list_path = listdir(rst_directory)
# total_files = 5
# file_counter = 1
# for file in list_path:
#     if file_counter > total_files:
#         continue
#     destination = path.join(rst_directory, file)
#     rst_text = parse_rs3(destination, True, output_location_bin)
#     raw_text = get_original_text(destination, output_location_raw)

#     file_counter += 1

# --------------------- END

# TODO This will only work if called_from_micrologic is true. We may want to reuse this code layer. Add a boolean (Called_from_micrologic) here to control that.
def RS3_generate_fis_training_data(tile_func, split_func, segmented_data=None, output_location=None, index=None):
    print(segmented_data)
    # TODO get the segments from the GUM files.
    # Implement the HILDA stuff for the case study. --> Use the Sentiment analysis method to compare my segmentations with theirs. -> FINISH PhD.
    to_string = get_original_text(segmented_data, None, True) # Called from micrologic (var. 3) is an assumption at this point.
    tree, processed_leaves = split_func(to_string, show=False)
    # We need to somehow get the true-bounds here for inputs of tile().
    tiled_data = tile_func(None, processed_leaves, None, 3, get_boundary=True)
    
    # GET THE ABS LOCATION FOR THIS]
    if not index:
        index = 'UNDEF'
    dotdat = open(path.join(output_location, f'train_{index}.dat'), 'w')
    
    data = ""
    for boundary_element in tiled_data:
        int_i = boundary_element['l_int']
        int_j = boundary_element['r_int']
        e_dis = boundary_element['e_dis']
        is_boundary = boundary_element['bound'][1]
        data += f'{is_boundary} {int_i} {int_j} {e_dis} \n'
    if output_location:
        dotdat.write(data)
    else:
        return data

def get_deps(location=None, rst_data=None):
    if location and not rst_data:
        pass
    elif rst_data and not location:
        pass
