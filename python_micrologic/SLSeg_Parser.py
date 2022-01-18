import re
import os
from nltk.tokenize import word_tokenize
import xml.etree.ElementTree as ET
# Create a bin representation of the slseg-parsed object.
# Indexed list produces a python list object of each segment in text-form.


def parse_slseg(location, bin=True, output_location=None):
    try:
        slseg = open(location, 'r')
        slseg = slseg.read()
        
        # slseg = re.sub(r'-', '', slseg)
        # slseg = re.sub(r'["]*', '', slseg)
        slseg = slseg.replace('<M>', '</C><C>')
        slseg = slseg.replace('</M>', '</C><C>')
        slseg = slseg.replace('&', 'and')
        parsed_slseg = ET.fromstring(slseg)
        # print(type(parsed_slseg))
        segments = []
    
        for child in parsed_slseg:
            child_tag = child.tag
            child_attr = child.attrib
            # Enforce str type.
            if bin:
                segments = '1'
            if child_tag == 'P':
                # parse the segments in this section
                for sentence in child:
                    for segment_tag in sentence:
                        # print (segment_tag.text)
                        if segment_tag.tag == 'C':
                            segement_text = segment_tag.text
                            if not bin:
                                segments.append(segement_text)
                            elif segement_text:
                                print (segement_text)
                                segments += '0'*(len(segement_text.strip().split(' '))-1)
                                segments += '1'
        if output_location:
            print(f'saving segments at {output_location}')
            file_name = location.split('/')
            # print(file_name)
            file_name = file_name[len(file_name)-1]
            output_location = os.path.join(output_location, file_name)
            output_location = open(output_location, 'w')
            output_location.write(segments)
            output_location.close()

            print(f'segments saved {file_name}\n')
  
        return segments
    except:
        pass

def SLSEG_generate_fis_training_data(segmented_data=None):
    pass
