function calculated_boundaries = run(fis, input_test_data)
    test_data = load(input_test_data);
    validation_data = test_data(:, 1); 
    test_input = test_data(:, 2:4);
    output_boundaries = [];
    for i = 1:length(test_input);
        calc_boundary = fis.evalfis();
        output_boundaries(i) = calc_boundary;
    end

    calculated_boundaries = output_boundaries;
end