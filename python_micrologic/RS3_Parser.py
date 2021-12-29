import io
from os import write, path, listdir
import xml.etree.ElementTree as ET

# Retrieve the segmentations from the RST file.
# if Bin, return the FuzzySeg version (binary), otherwise return a parsed list
# Output_location is not including the file name itself. This is taken from the location.
# The location variable includes the file name we are parsing.


def parse_rs3(location, bin=True, output_location=None):
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
                    segement_text = segment_tag.text
                    if not bin:
                        segments.append(segement_text)
                    elif segement_text:
                        segments += '0'*(len(segement_text.split(' '))-1)
                        # segments += '0'*len(segement_text.split(' '))
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


def get_original_text(location=None, write_to_file=None):
    rst = ET.parse(location)
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
            segement_text = segment_tag.text
            if segement_text != None:
                original_text += segement_text

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


# This code parses the GUM RST bits and produces the raw versions
# (To be segmented by SLSeg and SEGBot?) and produces the BIN outs from the already GUM-parsed text (taken from the GUM-RST outs)
rst_directory = '../dependencies/phd_datasets/gum_dataset/rst/rstweb/'
output_location_raw = '../dependencies/phd_datasets/gum_outputs/original_gum_text/'
output_location_bin = '../dependencies/phd_datasets/gum_outputs/original_gum_text_bin/'
list_path = listdir(rst_directory)
total_files = 5
file_counter = 1
for file in list_path:
    if file_counter > total_files:
        continue
    destination = path.join(rst_directory, file)
    rst_text = parse_rs3(destination, True, output_location_bin)
    raw_text = get_original_text(destination, output_location_raw)

    file_counter += 1
# --------------------- END


def get_deps(location=None, rst_data=None):
    if location and not rst_data:
        pass
    elif rst_data and not location:
        pass
