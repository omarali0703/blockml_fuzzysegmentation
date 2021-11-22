INPUT_FLOW = ""
OUTPUT_FLOW = "results"
# The order the subblocks are to be run in.

# Order that blocks are run.
BLOCK_ORDER = ["block_text_tilling", ]
# If specified, run command will take an extra argument to allow the use to choose which flow they would like to parser the outputs of the most recently executed block into.
POSSIBLE_PATH_MODE = ["block_syntax_parser", "block_dependency_parser"]

# Entry point for a block
test_looper = 1
def start(input_data=None, settings={}, loop_breaker):
    print(f"RUNNING.... My input data is\n{input_data}")

    if test_looper > 3:
        return 1, True
    else:
        test_looper += 1