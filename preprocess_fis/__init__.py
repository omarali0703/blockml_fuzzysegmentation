import json
import os
from . import ss2fb
from . import block_slseg_wrapper
INPUT_FLOW = None
OUTPUT_FLOW = None
# Entry point for a block
def start(input_data, settings):
    output_data, loop_breaker = {}, None
    input_data_location = settings['input_data_location']
    if settings['is_dir']:
        input_data_keys = os.listdir(input_data_location)
    else:
        input_data_keys = list(input_data.keys())
    if 'type' not in settings:
        print('Please specify a parser type')
        return
    if settings['type'] == 'syntax':
        for sub_path in input_data_keys:
            print(sub_path)
            # if settings['is_dir']:
            #     file_data = open(os.path.join(input_data, sub_path), 'r')
            # else:
            #     file_data = input_data[sub_path]
            # slsegged_file_data, loop_breaker = block_slseg_wrapper.run_slseg(
            #     path_to_slseg_source=os.path.join(settings['root'], 'SLSeg_ver_0.2'), test_samples=input_data_location, output_test=settings['slseg_output'])
            output_slseg_boundaries = open(os.path.join(settings['root'],settings['slseg_output'], f'binary/{sub_path.split(".")[0]}_bin.segdat'), 'w')
            
            boundary_objects, raw_bounds, raw_text = ss2fb.obtain_boundary_objects(
                None, slsegged_file_data, None, gum=True, slseg=False, k=3, get_boundary=False, write_to_file="dependencies.")
            output_slseg_boundaries.write(raw_bounds)
            continue # TODO Implement segbot model here. Raw text below could be switched to the raw text created by Rs3 Parser?
            segbot_input = run_segbot_model(raw_text)
            segbot_output = ss2fb.convert_segbot_2_bin(segbot_input)
            output_data[sub_path] = segbot_output
            segbot_output_path = settings['segbot_output_path']
            merged_output = f"{segbot_output_path}/segbot_classify_boundaries_{sub_path.split('.')[0]}.segdat"
            segbot_output_file = open(merged_output, 'w')

    return output_data, loop_breaker
