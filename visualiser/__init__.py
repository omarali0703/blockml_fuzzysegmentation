INPUT_FLOW = ""
OUTPUT_FLOW = "train"
# The order the subblocks are to be run in.
BLOCK_ORDER = ["block_visualiser", ]


# Entry point for a block
def start(input_data=None, settings={}):
    print('Producing results visualisations...')
