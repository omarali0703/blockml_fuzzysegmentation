import re, os
from nltk.tokenize import word_tokenize
import xml.etree.ElementTree as ET

# Create a bin representation of the slseg-parsed object.
# Indexed list produces a python list object of each segment in text-form.
segEx = '''
<T>
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

def parse_slseg(slseg, bin=True, output_location=None):
    slseg = re.sub(r'-', '', slseg)
    slseg = re.sub(r'["]*', '', slseg)
    slseg = re.sub(r'[\'`]*', '', slseg)
    slseg = slseg.replace(':', '')
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
                    print (segment_tag.text)
                    if segment_tag.tag == 'C':
                        segement_text = segment_tag.text
                        if not bin:
                            segments.append(segement_text)
                        elif segement_text:
                            segments += '0'*(len(segement_text.split(' '))-1)
                            segments += '1'
    print (segments)
    if output_location:
        print('saving segments...')
        file_name = output_location.split('/')
        print(file_name)
        file_name = file_name[len(file_name)-1]
        output_location = os.path.join(output_location, file_name)
        output_location = open(output_location, 'w')
        output_location.write(segments)
        output_location.close()

        print(f'segments saved {file_name}')
    return segments

parse_slseg(segEx,)