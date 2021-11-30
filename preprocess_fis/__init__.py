import json, os
from .block_text_tilling import *
INPUT_FLOW = None
OUTPUT_FLOW = None


# Entry point for a block
def start(input_data=None, settings={}):
    # list_path = os.listdir(dataset_path)
    output_data, loop_breaker = {}, None
    print("fuuuuuu", settings)
    input_data_keys = list(input_data.keys())
    if settings == 'syntax':
        for sub_path in input_data_keys:
            print(sub_path)
            file_data = input_data[sub_path]
            print(file_data, sub_path)
            boundary_objects, raw_bounds, raw_text = block_text_tilling.ss2fb.obtain_boundary_objects(None, file_data, None, slseg=True, k=3, get_boundary=False)
            print(raw_bounds)

            # merged_output = f"{output_path}/classify_boundaries_{sub_path.split('.')[0]}.arff"
            # ss2fb.write_as_arff(['index NUMERIC', 'bound_no_bound {boundary,no_boundary}', 'inti NUMERIC',
            #            'intj NUMERIC', 'ext NUMERIC'], boundary_objects, merged_output)
            segbot_input = run_segbot_model(raw_text)
            segbot_output = ss2fb.convert_segbot_2_bin(segbot_input)
            output_data[sub_path] = segbot_output
            merged_output = f"{output_path}/segbot_classify_boundaries_{sub_path.split('.')[0]}.segdat"
            segbot_output_file = open(merged_output, 'w')

    return output_data, loop_breaker