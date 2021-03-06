import io
import gc
from os import write, path, listdir
import xml.etree.ElementTree as ET
from progress.bar import Bar

# from ..preprocess_fis.block_text_tilling import tile, split
# from ..preprocess_fis.block_text_tilling import *
# Retrieve the segmentations from the RST file.
# if Bin, return the FuzzySeg version (binary), otherwise return a parsed list
# Output_location is not including the file name itself. This is taken from the location.
# The location variable includes the file name we are parsing.


def parse_rs3(location, bin=True, output_location=None):
    # if 'vavau' not in location:
    #     return
    bin = True if bin == "True" or bin == "true" or bin ==True else False
    print ("to bin?", type(bin))
    try:
        # rst = ET.parse(location)
        # root = rst.getroot()
        context = iter(ET.iterparse(location, events=("start", "end")))
        event, root = next(context)
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
                #  Parse the RST structure here?
                #  RST Main structure is stored here. Links and deps are determined here.
                pass
        if output_location:
            print('saving segments...')
            file_name = location.split('/')
            print(file_name)
            file_name = file_name[len(file_name)-1]
            output_location = path.join(output_location, file_name)
            output_location = open(output_location, 'w')
            output_location.write(str(segments))
            output_location.close()
            # print(f'segments saved {file_name}')
        print (segments, len(segments))
        return segments
    except OSError as error:
        print (error)



def get_original_text(location=None, write_to_file=None, called_from_micrologic=False):
    print('Begin getting original text....')

    
    try:
        # rst = ET.parse(location)
        # root = rst.getroot()
        context = iter(ET.iterparse(location, events=("start", "end")))
        event, root = next(context)
        # print (root)
        # print(rst)
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
            # print(write_to_file)
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

import matlab.engine
eng = matlab.engine.start_matlab()

def RS3_generate_fis_training_data(tile_func, split_func, segmented_data=None, output_location=None, index='0', k_size=3, parse_type='syntax'):
    # print(segmented_data)
    # Implement the HILDA stuff for the case study. --> Use the Sentiment analysis method to compare my segmentations with theirs. -> FINISH PhD.
    with Bar('Loading data...', max=7) as bar:
    
        to_string = get_original_text(segmented_data, None, True) # Called from micrologic (var. 3) is an assumption at this point.
        bar.next()
        tree, processed_leaves = split_func(to_string, show=False, parse_type=parse_type)
        bar.next()
        true_boundaries = parse_rs3(segmented_data, bin=True, output_location=None) #Get the bin representation of the boundaries from the rs3 files.
        bar.next()
        boundaries, validate, tiled_data = tile_func(eng, None, tree, processed_leaves, k_size, get_boundary=True, true_boundaries=true_boundaries)
        
        # GET THE ABS LOCATION FOR THIS]
        print(f'Beginning outputs to bin file {output_location}')
    
        print(f'Output file created {output_location}')
        print(f'Initialising data')
        
        # data = ""
        data_to_write_to_file = ""
        # print ("EH", boundaries, validate, tiled_data)
        bar.next()
        for boundary_element in tiled_data['steps']:
            # print (boundary_element)

            int_i = boundary_element['l_int']
            int_j = boundary_element['r_int']
            e_dis = boundary_element['e_dis']
            is_boundary = boundary_element['bound']
            # print(f'Writing data... {is_boundary} {int_i} {int_j} {e_dis}')
            
            data_to_write_to_file += f'{is_boundary} {int_i} {int_j} {e_dis} \n'
        bar.next()
        print(f'Finished writing data')
        # gc.collect(generation=2)
        bar.next()

        if output_location:
            print(len(data_to_write_to_file.split('\n')))
            dotdat = open(path.join(output_location, f'train_{index}_k{k_size}_{parse_type}.dat'), 'w')
            dotdat.write(data_to_write_to_file)
            dotdat.close()
            bar.next()

        else:
            bar.next()

            return data_to_write_to_file

def get_deps(location=None, rst_data=None):
    if location and not rst_data:
        pass
    elif rst_data and not location:
        pass
