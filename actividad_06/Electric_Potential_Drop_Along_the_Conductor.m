%% Material Parameters and Physics Constants
% Theoretical Physics limits (Standard SI units)
sigma_SI = 44e6;        % Conductivity in Siemens/meter (S/m)
length_SI = 40;         % Length in meters (m)
area_SI = 150e-6;       % Cross-section in square meters (m^2)

% Engineering limits (REBT mixed units)
c_eng = 44;             % Conductivity in m/(Ohm * mm^2)
length_eng = 40;        % Length in meters (m)
area_eng = 150;         % Cross-section in square millimeters (mm^2)

%% Microscopic to Macroscopic Integration (Resistance Calculation)
% 1. Theoretical Resistance using pure SI (R = L / (\sigma * A))
R_theoretical = length_SI / (sigma_SI * area_SI);

% 2. Engineering Resistance using mixed units (R = L / (c * S))
R_engineering = length_eng / (c_eng * area_eng);

% Verify equivalence
fprintf('Resistance (Theoretical): %.6f Ohms\n', R_theoretical);
fprintf('Resistance (Engineering): %.6f Ohms\n\n', R_engineering);

%% Voltage Drop Evaluation
% Assume the building from the previous activity: 145 kW at 400V (cos_phi = 0.9)
P_total = 145000;       % Watts
V_line = 400;           % Volts
cos_phi = 0.9;          

% Calculate line current (Three-phase)
I_line = P_total / (sqrt(3) * V_line * cos_phi);

% Voltage Drop (Delta V = I * R)
% Because we are looking at the 3-phase line-to-line drop, the REBT formula 
% inherently applies the sqrt(3) factor inside the S = (P*L)/(c*e*V) derivation.
% For a single conductor's direct drop:
delta_V_conductor = I_line * R_theoretical;
delta_V_3phase_system = sqrt(3) * delta_V_conductor;

fprintf('Current (Ib): %.2f A\n', I_line);
fprintf('System Voltage Drop: %.2f V\n', delta_V_3phase_system);

%% Visualization of the Electric Potential Field
% Let's plot the linear drop of the electric potential along the cable
x_positions = linspace(0, length_SI, 100);
V_source = 400; 
% Potential drops linearly due to uniform E-field (E = J/sigma)
V_along_wire = V_source - (sqrt(3) * I_line * (x_positions ./ (sigma_SI * area_SI)));

figure;
plot(x_positions, V_along_wire, 'LineWidth', 2, 'Color', '#D95319');
grid on;
title('Electric Potential Drop Along the Conductor / Caída de Potencial a lo Largo del Conductor');
xlabel('Distance from Source / Distancia desde el Origen (m)');
ylabel('Voltage / Tensión (V)');