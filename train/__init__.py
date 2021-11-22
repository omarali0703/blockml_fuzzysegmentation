INPUT_FLOW = ""
OUTPUT_FLOW = "train"
# The order the subblocks are to be run in.
BLOCK_ORDER = ["block_matlab_fuzzy_trainer",]


# Entry point for a block
def start(input_data=None, settings={}):
    print('Train block is running.')
    return {"output":"Here is some output data from training"}
