%% cleanup
clear
%% Setup Parameters for C1 Circuit
% Cable properties (Copper H07V-K)
length_m = 20;
section_mm2 = 1.5;

% Using resistivity of copper at 70 degrees C for a worst-case scenario
rho_cu_70C = 0.021; 

% Total round-trip resistance of the wire
R_line = 2 * rho_cu_70C * (length_m / section_mm2); 

%% Supply and Load configuration
V_rms = 230;
f_hz = 50;
P_load = 2300; % Max expected load for a 10A circuit

% Equivalent resistance of the load
R_load = (V_rms^2) / P_load;

%% Calculate Steady-State Expectations
I_expected = V_rms / (R_line + R_load);
V_drop = I_expected * R_line;

fprintf('Resistencia total de la línea: %.3f Ohmios\n', R_line);
fprintf('Caída de tensión calculada: %.2f V\n', V_drop);
fprintf('Intensidad de línea: %.2f A\n', I_expected);


%% 
fprintf('Iniciando simulación programática...\n');

%% Execute the Simulink Model Programmatically
% Ensure your Simulink file is named exactly 'c1_simulation.slx'
% and is located in your current MATLAB working directory.
model_name = 'c1_simulation';

% The sim() command runs the model and returns the data to 'out'
out = sim(model_name);

fprintf('Simulación completada. Generando gráficas...\n');
%% Plot Simulation Results
% Note: Run your Simulink model before executing this section. 
% Assuming your model outputs 'out.tout', 'out.V_source', and 'out.V_load'
% For demonstration, generating synthetic data if 'out' does not exist yet

if ~exist('out', 'var')
    t = linspace(0, 0.1, 1000);
    V_source = V_rms * sqrt(2) * sin(2*pi*f_hz*t);
    V_load = (V_rms - V_drop) * sqrt(2) * sin(2*pi*f_hz*t);
else
    t = out.tout;
    V_source = out.V_source;
    V_load = out.V_load;
end

figure;
plot(t, V_source, 'b-', 'LineWidth', 1.5);
hold on;
plot(t, V_load, 'r--', 'LineWidth', 1.5);
grid on;

title('Simulación de Caída de Tensión - Circuito C1');
xlabel('Tiempo (s)');
ylabel('Tensión (V)');
legend('Tensión en el Cuadro (Origen)', 'Tensión en el Receptor (Carga)');