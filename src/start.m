sDataDefFile = ''; %Empty -> Data Generated into Model source file

%% Inputs
in_a = Simulink.Signal;
in_a.DataType = 'uint8';
in_a.Min = 1;
in_a.Max = 199;
in_a.CoderInfo.StorageClass = 'Custom';
in_a.CoderInfo.CustomStorageClass = 'ExportToFile';
in_a.CoderInfo.CustomAttributes.DefinitionFile = sDataDefFile; 
in_b = copy(in_a);

%% Outputs
out_a                = copy(in_a);
out_a.Min = [];
out_a.Max = [];
out_b                = copy(out_a);
