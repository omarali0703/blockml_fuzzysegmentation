# MLFlow Example Project Structure
1. each folder defines a particular block the interface will run through
    2. each block can contain sub-blocks, modules etc that will run in the order of your choosing -> Defined in the **__init__** file of the respective block.
    
    3. each block must take an input and output file defined in the **IO.py** file in the root of the folder


## Example commands I use

### Example of running syntax-parse training for fuzzy system
```bash
python3 mlflow.py run fuzzy_segmentation preprocess_fis phd_datasets/raw_dataset_inputs syntax
```


### Example of running dependency-parse training for fuzzy system
```bash
python3 mlflow.py run fuzzy_segmentation preprocess_fis phd_datasets/raw_dataset_inputs dependency
```

### Running SLSeg
```bash
python3 run_all.py ../phd_datasets/gum_outputs/original_gum_text ../phd_datasets/slseg_outputs/gum ./parser05Aug16 -T50
```

Run on smaller set that is used by Fuzzy Seg.
```bash
python3 run_all.py ../phd_datasets/gum_outputs/original_gum_text ../phd_datasets/slseg_outputs/gum ./parser05Aug16 -T50
```

### Running Segbot (GUM Dataset)
```bash
python3 run_segbot.py '../phd_datasets/gum_outputs/original_gum_text' '../phd_datasets/segbot_outputs/gum' 
```

### Training and running fuzzy segmentation 

This will run all of them in a file and produce outputs.

```bash
python3 mlflow.py run fuzzy_segmentation train "phd_datasets/fuzzyseg_outputs/fis_training/" '{"none":"none"}'
```

This will only run using the one dataset. We only want to train once in this instance.

```bash
python3 mlflow.py run fuzzy_segmentation train "phd_datasets/fuzzyseg_outputs/fis_training/train_0-1_k3.dat" '{"training_data_path":"../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/train_0-1_k3.dat", "test_data_path":"../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/train_2_k3.dat"}'
```

Run the run + validation flow

```bash
python3 mlflow.py run-flow fuzzy_segmentation train-and-run-flow-syntax "phd_datasets/fuzzyseg_outputs/fis_training/charniak/train_0-1_k3_char.dat" '{"training_data_path":"../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/charniak/train_0-1_k3_char.dat", "test_data_path":"../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/charniak/train_2_k3_char.dat"}'

python3 mlflow.py run-flow fuzzy_segmentation train-and-run-flow-syntax "phd_datasets/fuzzyseg_outputs/fis_training/charniak/train_0-1_k5_char.dat" '{"training_data_path":"../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/charniak/train_0-1_k5_char.dat", "test_data_path":"../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/charniak/train_2_k5_char.dat"}'

python3 mlflow.py run-flow fuzzy_segmentation train-and-run-flow-syntax "phd_datasets/fuzzyseg_outputs/fis_training/syntax/train_0-1_k3.dat" '{"training_data_path":"../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/syntax/train_0-1_k3.dat", "test_data_path":"../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/syntax/train_2_k3.dat"}'
```