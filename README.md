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

### Running SLSeg & Segbot with Settings (Using the preprocess block) (GUM Dataset)
```bash
python3 mlflow.py run fuzzy_segmentation preprocess_fis 'phd_datasets/gum_outputs/original_gum_text' '{"type":"syntax", "is_dir":"True", "slseg_output":"phd_datasets/slseg_outputs/gum", "segbot_output_path":"phd_datasets/segbot_outputs/gum"}'
```