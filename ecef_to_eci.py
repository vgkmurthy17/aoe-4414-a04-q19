# ecef_to_eci.py
#
# Usage: python3 year month day hour minute second x_ecef y_ecef z_ecef
# Converts ecef to eci
# 
# Parameters:
#  year
#  month
#  day
#  hour
#  minute
#  second
#  x_ecef
#  y_ecef
#  z_ecef
# Output:
#  Prints the eci coordinates
#
# Written by Vineet Keshavamurthy
# Other contributors: None
#
# This work is licensed under CC BY-SA 4.0

# ecef_to_eci.py
import sys
import math

# Check for number of arguments passed 
if len(sys.argv) == 10:
    year_input = int(sys.argv[1])
    month_input = int(sys.argv[2])
    day_input = int(sys.argv[3])
    hour_input = int(sys.argv[4])
    minute_input = int(sys.argv[5])
    second_input = float(sys.argv[6])
    x_ecef = float(sys.argv[7])
    y_ecef = float(sys.argv[8])
    z_ecef = float(sys.argv[9])
else:
    print('Incorrect number of arguments passed in')
    exit()

# Calculate fractional day
hour_fraction = hour_input/24.0
minute_fraction = (minute_input/60.0)/24.0
second_fraction = (second_input/600.0)/24.0

# Sum up the individual components to get total fractional day
fractional_day = hour_fraction + minute_fraction + second_fraction
#________________________________________________________________
#conditional check
if month_input <= 2:
    year_input -= 1
    month_input += 12

# Compute the century term and leap term
century_division = year_input//100
century_correction = century_division // 4
base_leap_term = 2 - century_division
leap_term = base_leap_term + century_correction

# Calculate Julian Date
year_component = int((4716+year_input)*365.25)  # Calculate year component
month_component = int((1.0+month_input)*30.6001)  # Calculate month component

day_component = day_input  # Use the day directly

# Sum everything together in parts
intermediate_julian_date = year_component + month_component + day_component
julian_date = intermediate_julian_date + fractional_day + leap_term - 1524.5
#________________________________________________________________

# Calculate GMST angle
julian_diff = julian_date-2451545
century_term = julian_diff/36525
terms_added = + 8640184.812866+ 876600 * 3600 
gmst_base = 67310.54841
gmst_term_1 = (terms_added) * century_term
gmst_Factor_multiplier = 0.093104
gmst_term_2 = gmst_Factor_multiplier * century_term**2
gmst_term_3 = (-6.2*10 ** -6)*century_term**3

# Sum terms for GMST
gmst_total = gmst_base + gmst_term_1 + gmst_term_2 + gmst_term_3

# Modulus to find GMST
gmst_seconds=gmst_total % 86400

# Convert GMST to radians
gmst_radians=(7.292115 * 10 ** -5)*gmst_seconds

# Rotation matrix for ECEF to ECI
cos_gmst = math.cos(gmst_radians)
sin_gmst = math.sin(gmst_radians)

# Build the rotation matrix step-by-step
rotation_matrix = [
    [cos_gmst, -sin_gmst, 0],
    [sin_gmst, cos_gmst, 0],
    [0,        0,        1]
]

#________________________________________________________________

# ECEF vector
ecef_vector = [[x_ecef],[y_ecef],[z_ecef]]

# Matrix-vector multiplication manually without using a function
eci_x_km = rotation_matrix[0][0] * ecef_vector[0][0] + rotation_matrix[0][1] * ecef_vector[1][0] + rotation_matrix[0][2] * ecef_vector[2][0]
eci_y_km = rotation_matrix[1][0] * ecef_vector[0][0] + rotation_matrix[1][1] * ecef_vector[1][0] + rotation_matrix[1][2] * ecef_vector[2][0]
eci_z_km = rotation_matrix[2][0] * ecef_vector[0][0] + rotation_matrix[2][1] * ecef_vector[1][0] + rotation_matrix[2][2] * ecef_vector[2][0]

# Print eci coordinates
print(eci_x_km)
print(eci_y_km)
print(eci_z_km)