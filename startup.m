% check if conan is available
[status, ~] = system('which conan');
if status ~= 0 && ~contains(getenv('PATH'), '/opt/homebrew/bin')
    % add homebrew bin folder (needed to work on mac os)
    setenv('PATH', [getenv('PATH') ':/opt/homebrew/bin']);
    disp('added homebrew stuff to path');
end

% run conan install and dump output to log file
[status, output] = system('conan install .');
if status ~= 0
    % warn in case of problems
    disp('Could not resolve dependencies with Conan:');
    disp(output);
end
