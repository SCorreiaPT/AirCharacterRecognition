# ==============================================================================
# Laboratory of Electronics and Instrumentation (LEI)
# Portalegre Polytechnic University
# S. D. Correia, and J. P. Matos-Carvalho
# ==============================================================================
# Copyright 2025 LEI. All Rights Reserved.
# Licensed under the Apache License, Version 2.0
# ==============================================================================
import os
import glob
from dataAug import load_imu_data, augment_data

## @file main.py
## @brief Batch processor for IMU data augmentation.
## @details
## Scans a directory for CSV files (AirChar format),
## loads each file, and applies augmentation using dataAug.py,
## preserving and updating the descriptive header text and filename.

# ==============================================================================
# 1) Define input and output directories
# ==============================================================================
input_dir = "samples"       # Folder with original CSV files
output_dir = "samplesAug"   # Folder for augmented files
os.makedirs(output_dir, exist_ok=True)

# ==============================================================================
# 2) Find all CSV files in the input directory
# ==============================================================================
csv_files = glob.glob(os.path.join(input_dir, "*.csv"))
print(f"Found {len(csv_files)} CSV files in '{input_dir}'.")

# ==============================================================================
# 3) Process each file
# ==============================================================================
for file_path in csv_files:
    original_filename = os.path.basename(file_path)
    print(f"\n=== Processing file: {original_filename} ===")
    try:
        df, header_lines = load_imu_data(file_path)
        augment_data(df, header_lines, output_dir, original_filename)
    except Exception as e:
        print(f"Error processing {original_filename}: {e}")

print("\nBatch data augmentation completed.")
