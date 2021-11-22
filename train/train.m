function trained = train(training_data_path)
    fcmdata = load(training_data_path);
    
    options = [NaN 25 0.001 0];
    outputdata = fcmdata(:,1);
    inputdata = fcmdata(:,2:4);
    
    [centers] = fcm(inputdata,2,options);
    
%     maxU = max(U);
%     index1 = find(U(1,:) == maxU);
%     index2 = find(U(1,:) == maxU);
    opt = genfisOptions('FCMClustering', 'FISType', 'mamdani');
    opt.NumClusters = 2;
    opt.Verbose = 0;
    
    fis = genfis(centers, outputdata, opt);
    showrule(fis);
    
    fisT2 = convertToType2(fis);
    trained = fisT2;
end
