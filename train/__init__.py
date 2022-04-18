import os.path
import matlab.engine
import matlab
import numpy as np
import json

from progress.bar import Bar
INPUT_FLOW = ""
OUTPUT_FLOW = "train"
# The order the subblocks are to be run in.
BLOCK_ORDER = ["block_matlab_fuzzy_trainer", ]

eng = matlab.engine.start_matlab()

# Entry point for a block

from sklearn.model_selection import KFold

def fseg_to_matlab(data_arr):
    data_out = []
    for row in data_arr:
        data_out.append([float(i) for i in (row.strip().split(' '))])
    data_out = matlab.double(data_out)
    # print (data_out)
    return data_out

def start(input_data=None, settings={}):
    print (settings)
    with Bar('Loading data...', max=3) as bar:
        print (settings['training_data_path'])
        kfold=None
        kfold_value = None
        
        if 'kfold' in settings:
            kfold = settings['kfold']
        eng.cd('/Users/omarali/Documents/mlflow_source/mlflow_projects/fuzzy_segmentation/train')
        kfold_training_data = None
        kfold_test_data = None
        calculated_boundaries = []
        ref_boundaries = []
        if kfold:
            kfold_value = kfold

            kfold = KFold(n_splits=kfold, shuffle=True, random_state=None)
            localised_dir = os.path.join(settings['root'], settings['training_data_path'])
            # print (localised_dir)
            data = open(localised_dir, 'r').read()
            data = data.split('\n')
            # data = np.array(data)
            # print (data)
            for train, test in kfold.split(data):
                # print (f"train:\n{train}\ntest\n{test}")
                kfold_training_data = [data[index] for index, row in enumerate(train) if index in train]
                kfold_test_data = [data[index] for index, row in enumerate(test) if index in train]
                # print (f"train\n{kfold_training_data}test\n{kfold_test_data}\n")
                # return
                kfold_training_data = fseg_to_matlab(kfold_training_data)
                kfold_test_data = fseg_to_matlab(kfold_test_data)
                bar.next()
                # print (kfold_training_data)
                fuzzy_system = eng.train(kfold_training_data, True)
                bar.next()
                fold_calculated_boundaries, fold_ref_boundaries = eng.run(fuzzy_system, kfold_test_data, True, nargout=2)
                fold_calculated_boundaries = np.asarray(fold_calculated_boundaries[0]).tolist()[0]
                fold_ref_boundaries = np.asarray(fold_ref_boundaries[0]).tolist()[0]
                
                calculated_boundaries.append(fold_calculated_boundaries)
                ref_boundaries.append(fold_ref_boundaries)

        else:
            fuzzy_system = eng.train(settings['training_data_path'], False)

            calculated_boundaries, ref_boundaries = eng.run(fuzzy_system, settings['test_data_path'], False, nargout=2)
            calculated_boundaries = np.asarray(calculated_boundaries[0]).tolist()
            ref_boundaries = np.asarray(ref_boundaries[0]).tolist()

           
        bar.next()

        fuzzy_thresh = 0.655

        if kfold:
            print (calculated_boundaries, len(calculated_boundaries))
            for calc_boundary_set in calculated_boundaries:
                index = 0
                # print (calc_boundary_set)
                for calc_boundary in calc_boundary_set:
                    # print (calc_boundary)
                    if calc_boundary > fuzzy_thresh:
                        calc_boundary_set[index] = 1
                    else:
                        calc_boundary_set[index] = 0
                    index += 1
            
        else:
            index = 0
            for calc_boundary in calculated_boundaries:
                if calc_boundary > fuzzy_thresh:
                    calculated_boundaries[index] = 1
                else:
                    calculated_boundaries[index] = 0
                index += 1

        return json.dumps({"training_test_output": calculated_boundaries, "training_ref_outputs":ref_boundaries, "test_output_length":len(calculated_boundaries), "kfold":kfold_value}), None
