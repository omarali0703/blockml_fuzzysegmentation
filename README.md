# mlflow example project structure
1. each folder defines a particular block the interface will run through
    2. each block can contain sub-blocks, modules etc that will run in the order of your choosing -> Defined in the **__init__** file of the respective block.
    
    3. each block must take an input and output file defined in the **IO.py** file in the root of the folder


## Example commands I use

### Example of running syntax-parse training for fuzzy system
```
python3 mlflow.py run fuzzy_segmentation preprocess_fis phd_datasets/raw_dataset_inputs syntax
```

### Example of running dependency-parse training for fuzzy system
```
python3 mlflow.py run fuzzy_segmentation preprocess_fis phd_datasets/raw_dataset_inputs dependency
```