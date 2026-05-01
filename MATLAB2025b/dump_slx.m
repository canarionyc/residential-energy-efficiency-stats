%% Script para volcar el contenido de un modelo Simulink a texto
modelName = 'c1_simulation';
load_system(modelName);

fprintf('\n==================================================\n');
fprintf('INFORME DE BLOQUES EN: %s.slx\n', modelName);
fprintf('==================================================\n');

% Extraer todos los bloques del modelo
blocks = find_system(modelName, 'Type', 'Block');

%% Bucle para imprimir cada bloque (empezamos en 2 para omitir la raíz del modelo)

for i = 2:length(blocks)
    % Limpiar la ruta para que sea más legible
    blockName = strrep(blocks{i}, [modelName '/'], '');
    
    % En la librería SPS, la identidad real del bloque está en la "Máscara"
    maskType = get_param(blocks{i}, 'MaskType');
    blockType = get_param(blocks{i}, 'BlockType');
    
    if ~isempty(maskType)
        typeStr = maskType;
    else
        typeStr = blockType;
    end
    
	% Reemplazamos los saltos de línea ocultos por un espacio en blanco
    blockName = strrep(blockName, newline, ' ');
    typeStr = strrep(typeStr, newline, ' ');

    fprintf('• %s  ---->  [%s]\n', blockName, typeStr);
end
fprintf('==================================================\n\n');
fprintf('Copia el resultado de arriba y pégalo en el chat.\n');