import sys
import results2csv
# take an input segmentation, and a ground truth segmentation to validate.
def window_diff(true_segmentation, proposed_segmentation, k, boundary="1"):
    
    # print(true_segmentation, proposed_segmentation)
    if len(true_segmentation) != len(proposed_segmentation):
        print("error")
        # raise ValueError("Segmentations have unequal length")
    wd = 0
    for i in range(len(true_segmentation) - k):
        wd += abs(true_segmentation[i:i+k+1].count(boundary) - proposed_segmentation[i:i+k+1].count(boundary))
    return 1 - (1 / (len(true_segmentation) - k)) * wd

test_1 = '000001001000000'
test_2 = '000001001000010'

# print(window_diff(test_1, test_2, 1))

def window_pr(proposed_segmentation, true_segmentation):
    pass

# Traditional metric used everywhere.
def beefermans(proposed_segmentation, true_segmentation):
    pass

# Method that obtains the prec recall and accuracy using naive maths.
def basic_metric(proposed_segmentation, true_segmentation):
    h = proposed_segmentation.count('1') # Total computed bondaries
    g = true_segmentation.count('1') # Total reference bondaries
    c = 0 # Correctly identified segmentations
    if len(proposed_segmentation) != len(true_segmentation):
        sys.exit("Computed and reference boundaries must have the same length.")
    
    # Iterate to find the correct and incorrect segmentations
    h_index = 0
    for boundary in proposed_segmentation:  
        if boundary =='1' and true_segmentation[h_index] == boundary:
            c += 1
            
        h_index += 1
   
    precision = c / h
    recall = c / g
    f1_score = (2 * c) / (g + h)
    return (precision, recall, f1_score)


def run_all_validators(proposed_segmentation=None, true_segmentation=None, batch=False, translated_data_file=None, export=False, export_location=None):
   
    if batch and not translated_data_file:
        sys.exit("ERROR: Make sure a translated set of data is generated before running in batch mode.")

    elif not batch and (not proposed_segmentation or not true_segmentation):
        sys.exit("ERROR: If running in single-mode, make sure a computed and reference segmentation is provided")
    
    elif not batch and (proposed_segmentation and true_segmentation):
        # Run is singular mode
        window_diff =   basic_metric (proposed_segmentation, true_segmentation)
        window_pr =     window_pr    (proposed_segmentation, true_segmentation)
        beefermans =    beefermans   (proposed_segmentation, true_segmentation)
        basic_metric =  basic_metric (proposed_segmentation, true_segmentation)

        export_format = f"windowdiff,windowpr,beefermans,basicmetric,\n{window_diff},{window_pr},{beefermans},{basic_metric}"

        if export and not export_location:
            sys.exit("ERROR: please specify an exportable location.")
        elif export and export_location:
            write_to = open(export_location + '/exported.csv', 'w')
            write_to.write(export_format)
            write_to.close()
        

    elif batch and translated_data_file:
        pass
        # Run in batch mode
    else:
        sys.exit("ERROR: Unknown error occured.")

# print(basic_metric(test_1, test_2))
# print(window_diff(test_1, test_2, 2))