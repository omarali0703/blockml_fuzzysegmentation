# MLFlow Example Project Structure
1. each folder defines a particular block the interface will run through
    2. each block can contain sub-blocks, modules etc that will run in the order of your choosing -> Defined in the **__init__** file of the respective block.
    
    3. each block must take an input and output file defined in the **IO.py** file in the root of the folder


## Example commands I use

### Example of running syntax-parse training for fuzzy system
```bsh
python3 mlflow.py run fuzzy_segmentation preprocess_fis phd_datasets/raw_dataset_inputs syntax
```


### Example of running dependency-parse training for fuzzy system
```bsh
python3 mlflow.py run fuzzy_segmentation preprocess_fis phd_datasets/raw_dataset_inputs dependency
```

### Running SLSeg
```bsh
python3 run_all.py ../phd_datasets/gum_outputs/original_gum_text ../phd_datasets/slseg_outputs/gum ./parser05Aug16 -T50
```

> Run on smaller set that is used by Fuzzy Seg.
```bsh
python3 run_all.py ../phd_datasets/gum_outputs/original_gum_text ../phd_datasets/slseg_outputs/gum ./parser05Aug16 -T50
```

### Running Segbot (GUM Dataset)
```bsh
python3 run_segbot.py '../phd_datasets/gum_outputs/original_gum_text' '../phd_datasets/segbot_outputs/gum' 
```

### Running HILDA to generate the segmentations.

> Running hilda to get the segmentations

```bsh
python3 hilda.py -s texts/bbc_20081227.txt
```

### Training and running fuzzy segmentation 

> This will run all of them in a file and produce outputs --> This is specifically to return results (using kfold) for the original analysis of the model. This doesn't actually take in a file and segment it. That is below.

```bsh
python3 mlflow.py run fuzzy_segmentation train "phd_datasets/fuzzyseg_outputs/fis_training/" '{"none":"none"}'
```

This will only run using the one dataset. We only want to train once in this instance.

```bsh
python3 mlflow.py run fuzzy_segmentation train "phd_datasets/fuzzyseg_outputs/fis_training/train_0-1_k3.dat" '{"training_data_path":"../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/train_0-1_k3.dat", "test_data_path":"../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/train_2_k3.dat"}'
```

Run the run + validation flow

```bsh
python3 mlflow.py run-flow fuzzy_segmentation train-and-run-flow-syntax "phd_datasets/fuzzyseg_outputs/fis_training/charniak/train_0-1_k3_char.dat" '{"training_data_path":"../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/charniak/train_0-1_k3_char.dat", "test_data_path":"../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/charniak/train_2_k3_char.dat"}'

python3 mlflow.py run-flow fuzzy_segmentation train-and-run-flow-syntax "phd_datasets/fuzzyseg_outputs/fis_training/charniak/train_0-1_k5_char.dat" '{"training_data_path":"../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/charniak/train_0-1_k5_char.dat", "test_data_path":"../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/charniak/train_2_k5_char.dat"}'

python3 mlflow.py run-flow fuzzy_segmentation train-and-run-flow-syntax "phd_datasets/fuzzyseg_outputs/fis_training/syntax/train_0-1_k3.dat" '{"training_data_path":"../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/syntax/train_0-1_k3.dat", "test_data_path":"../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/syntax/train_2_k3.dat"}'

# KFOLD STUFF
python3 mlflow.py run-flow fuzzy_segmentation train-and-run-flow-syntax "../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/generated/train_12_k3_syntax.dat" '{"training_data_path":"phd_datasets/fuzzyseg_outputs/fis_training/generated/train_12_k3_syntax.dat", "test_data_path":"phd_datasets/fuzzyseg_outputs/fis_training/generated/test/train_12_k3_syntax.dat", "kfold":10}'


> this is using data that was generated before we did the fullstop logic (now commented out) in the comparewordavg function.
python3 mlflow.py run-flow fuzzy_segmentation train-and-run-flow-syntax "../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/generated/old_train_12_k3_syntax.dat" '{"training_data_path":"phd_datasets/fuzzyseg_outputs/fis_training/generated/old_train_12_k3_syntax.dat", "test_data_path":"phd_datasets/fuzzyseg_outputs/fis_training/generated/test/train_12_k3_syntax.dat", "kfold":10}'
# END KFOLD

python3 mlflow.py run-flow fuzzy_segmentation train-and-run-flow-syntax "phd_datasets/fuzzyseg_outputs/fis_training/academic/5050split/train_50_k3_syntax.dat" '{"training_data_path":"../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/academic/5050split/train_50_k3_syntax.dat", "test_data_path":"../dependencies/phd_datasets/fuzzyseg_outputs/fis_training/academic/5050split/test_50_k3_syntax.dat"}'
```


### Running FuzzySeg as a Segmenter

> To run FuzzySeg as a standalone piece. This process takes in a file + training data and returns a list of segments in HILDA or array format for use in subsequent RST or text summ. models. 


```bsh
python3 mlflow.py run fuzzy_segmentation run "phd_datasets/fuzzyseg_inputs/001a.txt" '{
    "training_data_path":"/phd_datasets/fuzzyseg_outputs/fis_training/generated/train_12_k3_syntax.dat", 
    "output_data_path":"/phd_datasets/fuzzyseg_outputs/gum",
    "parse_type":"syntax",
    "parser_output_form":"hilda"
}'

```