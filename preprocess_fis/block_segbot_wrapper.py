
def run_segbot(dataset_path, output_path=None):
    # dataset_path = "../../PhD Datasets/raw_dataset_inputs"
    # output_path = "../../PhD Datasets/segbot_outputs"
    list_path = os.listdir(dataset_path)

    segbot_source = __import__(
        '..dependencies.RunSegBot.run_segbot', fromlist=[''])

    for sub_path in list_path:
        # TODO Import dataset, run segbot on BBC dataset, outputs as bin in files that are index such that they can be read by fuzzyseg.
        file = open(f"{dataset_path}/{sub_path}", "r")
        file_data = file.read()
        file.close()

        output_seg = segbot_source.main_input_output(file_data)

        if not output_path:
            return output_seg

        output_seg_file = open(f"{output_path}/{sub_path}_sb.txt", "w")
        output_seg_file.truncate(0)
        for discourse_unit in output_seg:
            output_seg_file.write(f"{discourse_unit}\n")

        output_seg_file.close()
