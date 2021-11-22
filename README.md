# mlflow example project structure
1. each folder defines a particular block the interface will run through
    2. each block can contain sub-blocks, modules etc that will run in the order of your choosing -> Defined in the **__init__** file of the respective block.
    
    3. each block must take an input and output file defined in the **IO.py** file in the root of the folder