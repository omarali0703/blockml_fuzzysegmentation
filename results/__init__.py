INPUT_FLOW = "run"
OUTPUT_FLOW = ""
BLOCK_ORDER = ["sub_proccess_a", "sub_proccess_b"]  # The order the subblocks are to be run in.
                                                    # Sub-proccesses in this instance can consist of outputting data
                                                    # in a desired format
                                                    # etc.                                                    


# Entry point for a block
def start(input_data=None, settings={}):
    print('Results block is running.')
    