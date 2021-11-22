# Starting block to run
STARTING_BLOCK = 'preprocess'
# location of dependency files. Any datasets, images, or extra files apart from logic, should be stored here.
DEPENDENCIES = 'dependencies'
FLOW_ORDER = ["preprocess", "train", "run", "results", "visualiser"]
# Need a way to abstract a loop. Sub-list??