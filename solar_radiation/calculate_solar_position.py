import math

def calculate_solar_position(day_of_year, clock_hour_decimal, latitude=28.46, longitude=-16.25, tz_meridian=0.0):
    """
    Calculates Solar Declination, Equation of Time (Analemma coordinates), 
    and true Solar Altitude.
    """
    # Fractional year in radians
    gamma = (2 * math.pi / 366) * day_of_year
    
    # Solar Declination approximation (degrees)
    declination = (0.396372 - 22.91327 * math.cos(gamma) + 4.02543 * math.sin(gamma) 
                   - 0.387205 * math.cos(2*gamma) + 0.051967 * math.sin(2*gamma) 
                   - 0.154527 * math.cos(3*gamma) + 0.084798 * math.sin(3*gamma))
    print(f"declination: {declination}")
    # Equation of Time approximation (hours)
    time_eq_min = 60 * 3.819719 * (0.004289 + 0.125197 * math.cos(gamma) 
                                 - 1.52368 * math.sin(gamma) - 0.222714 * math.cos(2*gamma) 
                                 - 2.50294 * math.sin(2*gamma) - 0.046927 * math.cos(3*gamma) 
                                 - 0.165842 * math.sin(3*gamma))
    time_eq_hours = time_eq_min / 60
    
    # Hour Angle (H)
    # 1 hour = 15 degrees. Positive values are before solar noon.
    hour_angle = 15 * (12 - (clock_hour_decimal + time_eq_hours)) + (tz_meridian - longitude)
    print(f"hour_angle: {hour_angle}")
    # Solar Altitude (beta)
    lat_rad = math.radians(latitude)
    dec_rad = math.radians(declination)
    ha_rad = math.radians(hour_angle)
    
    sin_beta = (math.sin(lat_rad) * math.sin(dec_rad) + 
                math.cos(lat_rad) * math.cos(dec_rad) * math.cos(ha_rad))
    altitude = math.degrees(math.asin(sin_beta))
    print(f"declination: {declination}, time_eq_min: {time_eq_min}, altitude: {altitude}, hour_angle: {hour_angle}, lat_rad: {lat_rad}, dec_rad: {dec_rad}, ha_rad: {ha_rad}, sin_beta: {sin_beta}")
    return declination, time_eq_min, altitude

# Run for July 21st (Day 202) at 11:30 AM (11.5)
dec, eot, alt = calculate_solar_position(day_of_year=202, clock_hour_decimal=11.5)

print("--- Analemma & Solar Position ---")
print(f"Declination:      {dec:.2f}°")
print(f"Equation of Time: {eot:.2f} minutes")
print(f"Solar Altitude:   {alt:.2f}°")