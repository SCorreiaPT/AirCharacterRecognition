# ==============================================================================
# Laboratory of Electronics and Instrumentation (LEI)
# Portalegre Polytechnic University
# S. D. Correia, and J. P. Matos-Carvalho
# ==============================================================================
# Copyright 2025 LEI. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
# ==============================================================================
import pandas as pd
import numpy as np
import re
import os

## @file dataAug.py
## @brief Module for IMU data augmentation through 3D rotation.
## @details
## Loads IMU CSVs (AirChar format), extracts the descriptive header, applies
## augmentation via vector rotation, and saves new CSVs keeping the metadata header.

# ==============================================================================
def load_imu_data(csv_path: str):
    """
    @brief Load IMU data and extract descriptive header from an AirChar CSV.
    @param csv_path Path to the CSV file.
    @return (DataFrame, list[str]) Tuple containing numeric IMU data and header lines.
    """
    pattern = re.compile(r"^\s*-?\d+(\.\d+)?\s*;")
    header_lines = []
    data_start = None

    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        for idx, line in enumerate(f):
            if pattern.search(line):  # numeric data starts here
                data_start = idx
                break
            header_lines.append(line.strip())

    if data_start is None:
        raise RuntimeError("Could not locate numeric data section in the file.")

    colnames = ["label", "ax", "ay", "az", "gx", "gy", "gz"]
    df = pd.read_csv(csv_path, sep=";", header=None, names=colnames, skiprows=data_start, engine="python")

    return df, header_lines

# ==============================================================================
def rotation_matrix(axis: str, theta: float) -> np.ndarray:
    """
    @brief Compute a 3x3 rotation matrix.
    @param axis Axis of rotation ('x', 'y', or 'z').
    @param theta Rotation angle in radians.
    @return 3x3 NumPy array representing the rotation matrix.
    """
    ct, st = np.cos(theta), np.sin(theta)
    axis = axis.lower()
    if axis == "x":
        return np.array([[1, 0, 0], [0, ct, -st], [0, st, ct]])
    elif axis == "y":
        return np.array([[ct, 0, st], [0, 1, 0], [-st, 0, ct]])
    elif axis == "z":
        return np.array([[ct, -st, 0], [st, ct, 0], [0, 0, 1]])
    else:
        raise ValueError("Invalid axis. Use 'x', 'y', or 'z'.")

# ==============================================================================
def modify_header_for_augmentation(header_lines, axis: str, angle: int):
    """
    @brief Modify the metadata header to mark the file as augmented.
    @param header_lines Original header lines (list of strings).
    @param axis Rotation axis ('x', 'y', 'z').
    @param angle Rotation angle in degrees.
    @return List of updated header lines.
    """
    new_header = []
    aug_text = f"Augmentation: Yes ({axis}{angle:+d})"

    for line in header_lines:
        if line.lower().startswith("augmentation:"):
            new_header.append(aug_text)
        else:
            new_header.append(line)

    return new_header

# ==============================================================================
def build_augmented_filename(original_name: str, axis: str, angle: int) -> str:
    """
    @brief Build augmented filename replacing 'a0' with 'a{axis}{angle}'.
    @param original_name Base filename (e.g. A_s01v01n0001p0a0f0.csv)
    @param axis Rotation axis ('x', 'y', 'z')
    @param angle Rotation angle in degrees
    @return New filename string
    """
    # Extract name without extension
    name, ext = os.path.splitext(original_name)

    # Replace pattern 'a0' by 'a{axis}{angle}'
    new_name = re.sub(r"a0", f"a{axis}{angle:+d}", name)

    return new_name + ext

# ==============================================================================
def save_augmented_file(df_aug, header_lines, output_path):
    """
    @brief Save augmented IMU data with preserved and updated header.
    @param df_aug DataFrame with augmented IMU data.
    @param header_lines List of header strings.
    @param output_path Output CSV file path.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for line in header_lines:
            f.write(f"{line}\n")
        # Write numeric data block
        df_aug.to_csv(f, index=False, sep=";", header=False)

# ==============================================================================
def augment_data(df, header_lines, output_dir: str, original_filename: str):
    """
    @brief Apply data augmentation by rotating IMU data on multiple axes.
    @param df DataFrame containing IMU data.
    @param header_lines List of textual header lines.
    @param output_dir Directory to save augmented files.
    @param original_filename Name of the input file (used to build augmented name).
    @details
        Creates 18 augmented CSV files with rotations of ±15°, ±30°, ±45°
        around X, Y, and Z axes, preserving the descriptive header.
    """
    # axes = ['x', 'y', 'z']
    axes = ['x']
    angles_deg = [-10, -20, -30, -40, -50, -60, -70, -80, -90, 10, 20, 30, 40, 50, 60, 70, 80]

    count_generated = 0  # counter for augmented files

    for axis in axes:
        for angle in angles_deg:
            theta = np.deg2rad(angle)
            R = rotation_matrix(axis, theta)

            acc = df[['ax', 'ay', 'az']].to_numpy(dtype=float)
            gyr = df[['gx', 'gy', 'gz']].to_numpy(dtype=float)

            acc_rot = acc @ R.T
            gyr_rot = gyr @ R.T

            df_aug = df.copy()
            df_aug[['ax', 'ay', 'az']] = acc_rot
            df_aug[['gx', 'gy', 'gz']] = gyr_rot

            # Modify header for augmentation
            new_header = modify_header_for_augmentation(header_lines, axis, angle)

            # Generate new filename
            aug_filename = build_augmented_filename(original_filename, axis, angle)
            out_path = os.path.join(output_dir, aug_filename)

            # Save with modified header
            save_augmented_file(df_aug, new_header, out_path)
            print(f"Saved {out_path}")
            count_generated += 1

    print(f"All augmented datasets created successfully for {original_filename}")
    print(f"   → Total augmented files generated: {count_generated}\n")
