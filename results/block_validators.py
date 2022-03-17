import sys
import math
# take an input segmentation, and a ground truth segmentation to validate.
def window_diff(true_segmentation, proposed_segmentation, k=1, boundary=1):
    
    # print(true_segmentation, proposed_segmentation)
    if len(true_segmentation) != len(proposed_segmentation):
        sys.exit("Computed and reference boundaries must have the same length.")
        
        # raise ValueError("Segmentations have unequal length")
    wd = 0
    for i in range(len(true_segmentation) - k):
        wd += abs(true_segmentation[i:i+k+1].count(boundary) - proposed_segmentation[i:i+k+1].count(boundary))
    print (wd)
    return 1 - (1 / (len(true_segmentation) - k)) * wd

# test_1 = '000001001000000'
# test_2 = '000001001000010'

# print(window_diff(test_1, test_2, 1))

def window_pr(proposed_segmentation, true_segmentation, k=3, boundary=1):
    true_positive = 0
    true_negative = -k*(k-1)
    false_positive = 0
    false_negative = 0
    # print(true_segmentation, proposed_segmentation)
    if len(true_segmentation) != len(proposed_segmentation):
        sys.exit("Computed and reference boundaries must have the same length.")

    
    for i in range(1-k, len(true_segmentation)):
        true_positive += min(true_segmentation[i:i+k].count(boundary), proposed_segmentation[i:i+k].count(boundary))
        true_negative += k-max(true_segmentation[i:i+k].count(boundary), proposed_segmentation[i:i+k].count(boundary))
        false_positive += max(0, (true_segmentation[i:i+k].count(boundary) - proposed_segmentation[i:i+k].count(boundary)))
        false_negative += max(0, (proposed_segmentation[i:i+k].count(boundary) - true_segmentation[i:i+k].count(boundary)))
    
    precision = true_positive/(true_positive + false_positive)
    recall = true_positive/(true_positive + false_negative)
    accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)
    f1_score = true_positive/(true_positive + 0.5 * (false_positive+false_negative))

    return precision, recall, accuracy

# Traditional metric used everywhere.
def beefermans(proposed_segmentation, true_segmentation):
    return 'None'

# Method that obtains the prec recall and accuracy using naive maths.
def basic_metric(proposed_segmentation, true_segmentation, boundary=1):
    h = proposed_segmentation.count(boundary) # Total computed bondaries
    g = true_segmentation.count(boundary) # Total reference bondaries
    c = 0 # Correctly identified segmentations
    if len(proposed_segmentation) != len(true_segmentation):
        sys.exit("Computed and reference boundaries must have the same length.")
    
    # Iterate to find the correct and incorrect segmentations
    h_index = 0
    for b in proposed_segmentation:  
        b = int(b)
        # print (boundary, true_segmentation[h_index], true_segmentation[h_index] == int(boundary))
        if b==1 and true_segmentation[h_index] == boundary:
            # print('fuck')
            c += 1
            
        h_index += 1
    # print (c, h, g)
    precision = c / h
    recall = c / g

    f1_score = (2 * c) / (g + h)
    return precision, recall, f1_score


def run_all_validators(proposed_segmentation=None, true_segmentation=None, batch=False, translated_data_file=None, export=False, export_location=None):
   
    if batch and not translated_data_file:
        sys.exit("ERROR: Make sure a translated set of data is generated before running in batch mode.")

    elif not batch and (not proposed_segmentation or not true_segmentation):
        sys.exit("ERROR: If running in single-mode, make sure a computed and reference segmentation is provided")
    
    elif not batch and (proposed_segmentation and true_segmentation):
        # Run is singular mode
        window_diff_ =   window_diff   (proposed_segmentation, true_segmentation, k=1)
        window_pr_ =     window_pr    (proposed_segmentation, true_segmentation, k=3)
        beefermans_ =    beefermans   (proposed_segmentation, true_segmentation)
        basic_metric_p, basic_metric_r, basic_metric_a =  basic_metric (proposed_segmentation, true_segmentation)

        export_format = f"windowdiff,windowpr,beefermans,basicmetric_pre, basicmetric_rec, basicmetric_acc,\n{window_diff_},{window_pr_},{beefermans_},{basic_metric_p}, {basic_metric_r}, {basic_metric_a}"
        print (export_format)

        if export and not export_location:
            sys.exit("ERROR: please specify an exportable location.")
        elif export and export_location:
            write_to = open(export_location + 'exported.csv', 'w')
            write_to.write(export_format)
            write_to.close()
        
        return {"window_diff_":window_diff_, "window_pr_":window_pr_, "beefermans_":beefermans_, "basic_metric":(basic_metric_p, basic_metric_r, basic_metric_a)}

    elif batch and translated_data_file:
        pass
        # Run in batch mode
    else:
        sys.exit("ERROR: Unknown error occured.")

# print(basic_metric(test_1, test_2))
# print(window_diff(test_1, test_2, 2))