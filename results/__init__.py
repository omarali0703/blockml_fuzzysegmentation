INPUT_FLOW = "run"
OUTPUT_FLOW = ""
BLOCK_ORDER = ["sub_proccess_a", "sub_proccess_b"]  # The order the subblocks are to be run in.
                                                    # Sub-proccesses in this instance can consist of outputting data
                                                    # in a desired format
                                                    # etc.                                                    

from . import block_validators
import json 
# Entry point for a block
def start(input_data=None, settings={}):
    print('Results block is running.')
    input_data = json.loads(input_data)
    calculated = input_data['training_test_output']
    reference = input_data['training_ref_outputs']

    outputs = block_validators.run_all_validators(proposed_segmentation=calculated, true_segmentation=reference, batch=False, translated_data_file=None, export=True, export_location='./')

    return {}, None
    