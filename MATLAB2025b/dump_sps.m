%% SCRIPT DE VOLCADO DE LIBRERIA SPS
% Load the Specialized Power Systems core library into memory
load_system('powerlib');

% Extract all block paths within the library
sps_blocks = find_system('powerlib');
total_blocks = length(sps_blocks);

% Print the header in the command window
fprintf('==================================================\n');
fprintf('LIBRERÍA SPECIALIZED POWER SYSTEMS (SPS) CARGADA\n');
fprintf('==================================================\n');
fprintf('Total de bloques disponibles: %d\n\n', total_blocks);
fprintf('Ejemplo de las rutas principales para nuestra simulación:\n');

% Filter and display some key fundamental blocks for the REBT simulation
target_keywords = {'AC Voltage Source', 'Series RLC Branch', 'powergui', 'Voltage Measurement'};

for idx = 1:total_blocks
    current_block = sps_blocks{idx};
    
    % Check if the current block path contains any of our target keywords
    for k = 1:length(target_keywords)
        if contains(current_block, target_keywords{k}, 'IgnoreCase', true)
            fprintf('Bloque encontrado: %s\n', current_block);
            break; 
        end
    end
end

fprintf('\nPara abrir la interfaz gráfica de esta librería, escribe "powerlib" en la consola.\n');