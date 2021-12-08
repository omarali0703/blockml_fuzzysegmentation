import io
import xml.etree.ElementTree as ET

# Retrieve the segmentations from the RST file.
# if Bin, return the FuzzySeg version (binary), otherwise return a parsed list
def parse_rst(location, bin=True):
    rst = ET.parse(location)
    root = rst.getroot()
    segments = []
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
                else:
                    bin += '0'*len(segement_text.split(' '))
                    bin += '1'
                
        elif child_tag == 'head':
            # TODO Parse the RST structure here?
            pass
    return segments

def get_original_text(location=None, ):
    rst = ET.parse(location)
    root = rst.getroot()
    original_text = ''
    for child in root:
        child_tag = child.tag
        child_attr = child.attrib
        if child_tag == 'body':
            # parse the segments in this section
            for segment_tag in child:
                segement_text = segment_tag.text
                original_text += segement_text

    return original_text

def get_deps(location=None, rst_data=None):
    if location and not rst_data:
        pass
    elif rst_data and not location:
        pass
