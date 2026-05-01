%% SCRIPT DE VOLCADO EXHAUSTIVO SPS
% Load the Specialized Power Systems core library into memory
load_system('powerlib');

% Extract all block paths, forcing the search to look inside subsystems
all_sps_blocks = find_system('powerlib', 'LookUnderMasks', 'all', 'FollowLinks', 'on');
total_deep_blocks = length(all_sps_blocks);

% Print header
fprintf('==================================================\n');
fprintf('VOLCADO COMPLETO DE LIBRERÍA SPS (POWERLIB)\n');
fprintf('==================================================\n');
fprintf('Total de elementos encontrados: %d\n\n', total_deep_blocks);

% Loop through every single block and print its exact path
for idx = 1:total_deep_blocks
    fprintf('Ruta %d: %s\n', idx, all_sps_blocks{idx});
end

fprintf('\nVolcado finalizado. Desplázate hacia arriba en la consola para revisar los nombres.\n');