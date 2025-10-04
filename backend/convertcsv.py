import pandas as pd

# Input and output paths
input_file = "/Users/sdolia/Desktop/input.csv"   # <-- export your Numbers file as CSV first
output_file = "/Users/sdolia/Desktop/Filtered.csv"

# Read the CSV with proper handling of empty strings
df = pd.read_csv(input_file, keep_default_na=False, na_values=[''], dtype=str)

# The CSV data is misaligned, so we need to map to the correct columns:
# Student names are in "Mobile Phone" column (position 6)
# Grades are in "Gender" column (position 14) 
# Photo Release is in "Authorized to Pickup" column (position 18)
# Parent Pickup is in "Parent Pickup" column (position 17)

# Create a new DataFrame with the correct data
filtered_df = pd.DataFrame({
    'Student': df.iloc[:, 6],  # Mobile Phone column has student names
    'Grade': df.iloc[:, 14],   # Gender column has the actual grades
    'Photo Release': df.iloc[:, 18],  # Authorized to Pickup column has Photo Release
    'Parent Pickup': df.iloc[:, 17]  # Parent Pickup column is correct
})

# Save the filtered CSV, preserving empty strings as valid values
filtered_df.to_csv(output_file, index=False, na_rep='')

print("Filtered CSV created:", output_file)
