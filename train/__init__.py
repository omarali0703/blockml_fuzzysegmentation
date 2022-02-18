import os.path
import matlab.engine
from progress.bar import Bar
INPUT_FLOW = ""
OUTPUT_FLOW = "train"
# The order the subblocks are to be run in.
BLOCK_ORDER = ["block_matlab_fuzzy_trainer", ]

eng = matlab.engine.start_matlab()

# Entry point for a block


def start(input_data=None, settings={}):
    with Bar('Loading data...', max=3) as bar:
        print (settings['training_data_path'])
        eng.cd('/Users/omarali/Documents/mlflow_source/mlflow_projects/fuzzy_segmentation/train')
        fuzzy_system = eng.train(settings['training_data_path'])
        bar.next()
        print( fuzzy_system )
        bar.next()

        output_and_ref_boundaries = eng.run(fuzzy_system, settings['test_data_path'])
        return {"training_test_output": output_and_ref_boundaries}, None
