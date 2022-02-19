import os.path
import matlab.engine
import numpy as np
import json

from progress.bar import Bar
INPUT_FLOW = ""
OUTPUT_FLOW = "train"
# The order the subblocks are to be run in.
BLOCK_ORDER = ["block_matlab_fuzzy_trainer", ]

eng = matlab.engine.start_matlab()

# Entry point for a block


def start(input_data=None, settings={}):
    print (settings)
    with Bar('Loading data...', max=3) as bar:
        print (settings['training_data_path'])
        eng.cd('/Users/omarali/Documents/mlflow_source/mlflow_projects/fuzzy_segmentation/train')
        fuzzy_system = eng.train(settings['training_data_path'])
        bar.next()
        print( fuzzy_system )
        bar.next()

        calculated_boundaries, ref_boundaries = eng.run(fuzzy_system, settings['test_data_path'], nargout=2)
        calculated_boundaries = list(np.asarray(calculated_boundaries[0]))
        ref_boundaries = list(np.asarray(ref_boundaries[0]))
        
        fuzzy_thresh = 0.55
        index = 0
        for calc_boundary in calculated_boundaries:
            if calc_boundary > fuzzy_thresh:
                calculated_boundaries[index] = 1
            else:
                calculated_boundaries[index] = 0
            index += 1

        return json.dumps({"training_test_output": calculated_boundaries, "training_ref_outputs":ref_boundaries, "test_output_length":len(calculated_boundaries)}), None
