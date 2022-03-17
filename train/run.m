function [calculated_boundaries, reference_boundaries] = run(fuzzy_system, input_test_data, kfold)
    if kfold == false
        test_data = load(input_test_data);
    else
        test_data = input_test_data
        
    validation_data = test_data(:, 1); 
    test_input = test_data(:, 2:4);
    val_output = double.empty(0);
    test_input_length = length(test_input);
    output_boundaries = double.empty(0);
    for i = 1:length(test_input)
        % disp(test_input(i, 1));
        calc_boundary = evalfis(fuzzy_system, [test_input(i, 1) test_input(i, 2) test_input(i, 3)]);
        output_boundaries(:, i) = calc_boundary;
    end

    for i = 1: length(validation_data)
        val_output(:, i) = validation_data(i, 1);
    end

    calculated_boundaries = output_boundaries;
    reference_boundaries = val_output;
end