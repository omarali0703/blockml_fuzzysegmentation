INPUT_FLOW = "run"
OUTPUT_FLOW = ""
BLOCK_ORDER = ["sub_proccess_a", "sub_proccess_b"]  # The order the subblocks are to be run in.
                                                    # Sub-proccesses in this instance can consist of outputting data
                                                    # in a desired format
                                                    # etc.                                                    

from mlflow_projects.fuzzy_segmentation.preprocess_fis.block_text_tilling import calculate_boundary
from . import block_validators
import json 
# Entry point for a block
def average_outputs(outputs, k):
    wd_avg = 0
    winpr_avg = [0, 0, 0]
    bm_avg = [0, 0, 0]
    k = int(k)
    for row in outputs:
        wd_avg += row['window_diff_']
        for i, r in enumerate(row['window_pr_']):
            print (i, r)
            winpr_avg[i] += r
        for i, r in enumerate(row['basic_metric']):
            print(i, r)
            bm_avg[i] += r

    return f"WinDIFF: {wd_avg/k}\nWinPR: {[i/k for i in winpr_avg]}\BasicMETRIC: {[i/k for i in bm_avg]}"

def start(input_data=None, settings={}):
    print('Results block is running.')
    input_data = json.loads(input_data)
    calculated = input_data['training_test_output']
    reference = input_data['training_ref_outputs']
    kfold = input_data['kfold']
    outputs = []
    if kfold:
        for i in range(len(calculated)):
            # print (calculated[i], reference[i])
            outputs.append(block_validators.run_all_validators(proposed_segmentation=calculated[i], true_segmentation=reference[i], batch=False, translated_data_file=None, export=False, export_location=None))
        print(average_outputs(outputs, kfold))
    return {}, None
    