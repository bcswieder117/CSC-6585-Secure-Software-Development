# Blaine Swieder
# CSC 6585: Secure Software Development
# November 12th, 2024

"""
Differential Privacy Script

Usage:
    python DifferentialPrivacy2.py <filename> <index> <lower_bound> <upper_bound>

Example:
    python DifferentialPrivacy2.py gdp-2024.csv 2 -1000.0 1000.0

Arguments:
    filename       - This is the name of the CSV file containing the data.
    index          - This is the index of the column you want to analyze (0-based).
    lower_bound    - This is the minimum value for initial data filtering.
    upper_bound    - This is the maximum value for initial data filtering.

Description:
    This program calculates a differentially private mean of a specified column in our given CSV file.
    First, it filters the data based on the provided lower and upper bounds, then it dynamically
    computes separate bounds for the differential privacy computation, by using the interquartile
    range (IQR) method by default to exclude extreme values.

    The epsilon value or "privacy parameter" is set as a constant in the code; moreover, the computed bounds
    for differential privacy are separate from the command-line filtering bounds in order to ensure robust
    handling of outliers and stable privacy protection.

    Output:
    - The program prints the differentially private mean of the selected column.
"""

import sys
import pandas as pd
import numpy as np

# Set epsilon as a/the constant for privacy
EPSILON = 0.2  # This value controls the level of privacy as lower values add more noise for increased privacy.

# Function to calculate bounds for differential privacy
def calculate_bounds(data, method="iqr", lower_percentile=5, upper_percentile=95):
    """
    Calculate the upper and lower bounds based on the selected method.
    Method Choices:
    - "constant": Uses predefined fixed lower and upper bounds.
    - "range": Sets the bounds as the minimum and maximum of the data.
    - "percentile": Sets the bounds as the lower and upper percentiles of the data, making it robust to outliers.
    - "iqr": Uses the interquartile range (IQR) to exclude extreme outliers for a more stable privacy computation.
    
    In practice, differential privacy libraries typically use methods like "percentile" or "iqr" to calculate bounds
    in order to avoid extreme values that could distort results. By excluding outliers, these methods ensure that
    the added noise level remains consistent and does not disproportionately affect the final result.
    """
    
    if method == "constant":
        return -1000.0, 1000.0  # Example fixed bounds; adjust as needed.
    elif method == "range":
        return data.min(), data.max()
    elif method == "percentile":
        # Using percentiles provides flexibility for data with extreme values by limiting the bounds
        return np.percentile(data, lower_percentile), np.percentile(data, upper_percentile)
    elif method == "iqr":
        # The IQR method focuses on the middle 50% of the data, which provides a stable range for DP computations
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        return q1 - 1.5 * iqr, q3 + 1.5 * iqr
    else:
        raise ValueError("Invalid method for calculating bounds.")

def main():
    # Check for the correct number of command-line arguments
    if len(sys.argv) != 5:
        print("Usage: python DifferentialPrivacy2.py <filename> <index> <lower_bound> <upper_bound>")
        return

    # Parse command-line arguments
    filename = sys.argv[1]
    index = int(sys.argv[2])
    lower_bound = float(sys.argv[3])
    upper_bound = float(sys.argv[4])

    # Read the CSV file
    df = pd.read_csv(filename)

    # Extract the specified column and convert it to numeric, removing NaNs
    col = pd.to_numeric(df.iloc[:, index], errors='coerce').dropna()

    # Step 1: Filter data within the user-specified range (from command-line arguments)
    col_filtered = col[(col >= lower_bound) & (col <= upper_bound)]
    n = len(col_filtered)
    if n == 0:
        print("Error: No data points in the specified range.")
        return

    # Step 2: Calculate bounds for differential privacy computation
    # Using IQR as the default method for robust bounds
    dynamic_lower_bound, dynamic_upper_bound = calculate_bounds(col_filtered, method="iqr")

    # Step 3: Clip data to the computed bounds
    col_clipped = np.clip(col_filtered, dynamic_lower_bound, dynamic_upper_bound)

    # Step 4: Calculate the sensitivity for the sum (upper bound - lower bound)
    sensitivity = dynamic_upper_bound - dynamic_lower_bound

    # Step 5: Compute Laplace noise scale based on sensitivity and epsilon
    scale = sensitivity / EPSILON

    # Step 6: Add Laplace noise to the sum and compute the differentially private mean
    total = col_clipped.sum()
    noisy_total = total + np.random.laplace(0, scale)
    dp_mean = noisy_total / n

    # Print the differentially private mean
    print(f"Differentially Private Mean: {dp_mean}")

    # Additional Debugging Information (Optional)
    print(f"Dynamic Bounds Used: Lower = {dynamic_lower_bound}, Upper = {dynamic_upper_bound}")
    print(f"Sensitivity: {sensitivity}, Laplace Scale: {scale}")

if __name__ == "__main__":
    main()

