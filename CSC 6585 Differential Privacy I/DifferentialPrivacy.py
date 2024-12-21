# Blaine Swieder 
# 11/5/2024
# CSC 6585: Homework 9, Differential Privacy


# Usage:
# If you want to run this script, please use the following command format:
# python DifferentialPrivacy.py <filename> <index> <lower_bound> <upper_bound>
# Example usage:
# python DifferentialPrivacy.py gdp-2024.csv 2 -1000.0 1000.0

# You will neeed to ensure that 'pandas' and 'numpy' are installed in your Python environment:
# Run 'pip install pandas numpy' if necessary.

import sys
import pandas as pd
import numpy as np

def main():
    # Check the number of command-line arguments
    if len(sys.argv) != 5:
        print("Error: Incorrect number of arguments.")
        return

    # Parse command-line arguments
    filename = sys.argv[1]
    try:
        index = int(sys.argv[2])
    except ValueError:
        print("Error: Index must be an integer.")
        return

    try:
        lower_bound = float(sys.argv[3])
        upper_bound = float(sys.argv[4])
    except ValueError:
        print("Error: Lower and upper bounds must be floats.")
        return

    # Check that lower_bound <= upper_bound
    if lower_bound > upper_bound:
        print("Error: Lower bound is greater than upper bound.")
        return

    # Read the CSV file
    try:
        df = pd.read_csv(filename)
    except Exception:
        print("Error: Unable to read file.")
        return

    # Check if index is within range
    if index < 0 or index >= len(df.columns):
        print("Error: Index out of range.")
        return

    # Extract the specified column
    col = df.iloc[:, index]

    # Convert the column to numeric values, coerce errors to NaN
    col = pd.to_numeric(col, errors='coerce')

    # Drop NaN values
    col = col.dropna()

    # Filter data within the inclusive range
    col_filtered = col[(col >= lower_bound) & (col <= upper_bound)]

    n = len(col_filtered)
    if n == 0:
        print("Error: No data points in the specified range.")
        return

    # Compute mean and standard deviation
    mean = col_filtered.mean()
    std_dev = col_filtered.std(ddof=0)  # Population standard deviation

    # Compute sensitivity
    epsilon = 0.2
    sensitivity = (upper_bound - lower_bound) / n

    # Compute Laplace scale
    scale = sensitivity / epsilon

    # Add Laplace noise
    laplace_noise_mean = np.random.laplace(0, scale)
    laplace_noise_std = np.random.laplace(0, scale)

    dp_mean = mean + laplace_noise_mean
    dp_std_dev = std_dev + laplace_noise_std

    # Print the results
    print(dp_mean)
    print(dp_std_dev)

if __name__ == "__main__":
    main()
