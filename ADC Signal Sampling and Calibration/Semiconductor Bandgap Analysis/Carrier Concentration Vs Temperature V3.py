import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Boltzmann constant
kB = 8.617333262145e-5  # Boltzmann constant in eV/K

# Data: Temperature (K), Carrier Concentration (cm^-3), and uncertainties
T_values = np.array([138.609, 194.855, 233.76, 251.570, 263.89, 273.199, 281.637, 286.637,
                     294.522, 301.36, 307.007, 316.265, 322.712, 340.179,350.925])
T_uncertainties = np.array([0.385, 0.788, 0.200, 0.978, 0.35, 0.213, 0.117, 0.0082,
                            0.04, 0.224, 0.042, 0.270, 0.117, 0.214,0.043])
n_values = np.array([2.02922078e+14, 2.39026961e+14,
                                 2.51680805e+14, 2.27176157e+14, 2.43451790e+14,
                                 2.40189212e+14, 2.58755007e+14, 2.48165107e+14,
                                 7.70037427e+14, 6.57556960e+14, 1.27375814e+15,
                                 1.36842935e+15, 1.21201403e+15, 1.57608983e+15,22.8844682e+14])

n_uncertainties = np.array([1.3e+10, 1.8e+10, 
                                        2.0e+10, 1.7e+10, 1.9e+10,
                                        1.8e+10, 2.0e+10, 2.0e+10,
                                        1.9e+10, 1.4e+10, 5.0e+10,
                                        6.0e+10, 5.0e+10, 8.0e+10,17e10])*5000

# Define the nonlinear fit function with a constant term
def nonlinear_fit_with_constant(T, A, Eg, C):
    return A * T**(3/2) * np.exp(-Eg / (2 * kB * T)) + C

# Perform nonlinear fit for all data
initial_guess = [1e10, 0.7, 1e14] # Initial guesses for A (scaling factor), Eg (bandgap), and C (constant)
nonlinear_params, nonlinear_cov_matrix = curve_fit(
    nonlinear_fit_with_constant,
    T_values,
    n_values,
    p0=initial_guess,
    sigma=n_uncertainties,
    absolute_sigma=True
)

# Extract fitted parameters and their uncertainties
A_fit, Eg_fit, C_fit = nonlinear_params
A_uncertainty = np.sqrt(nonlinear_cov_matrix[0][0])
Eg_uncertainty = np.sqrt(nonlinear_cov_matrix[1][1])
C_uncertainty = np.sqrt(nonlinear_cov_matrix[2][2])

# Calculate residuals
nonlinear_residuals = n_values - nonlinear_fit_with_constant(T_values, A_fit, Eg_fit, C_fit)

# Generate fitted values for plotting
T_fine = np.linspace(min(T_values), max(T_values), 1000)
fitted_n_nonlinear = nonlinear_fit_with_constant(T_fine, A_fit, Eg_fit, C_fit)

# Calculate chi-squared statistic
chi_squared = np.sum((nonlinear_residuals / n_uncertainties)**2)

# Calculate degrees of freedom (n_observations - n_parameters)
dof = len(n_values) - len(nonlinear_params)

# Calculate reduced chi-squared
reduced_chi_squared = chi_squared / dof

# Plotting the results
plt.rcParams.update({'font.size': 34}) # Adjust font size for better readability

# Create figure with subplots
fig = plt.figure(figsize=(12,16))
gs = fig.add_gridspec(2, height_ratios=[2.,1], hspace=0.4)

# Main plot: Carrier Concentration vs Temperature
ax1 = fig.add_subplot(gs[0])
ax1.errorbar(
    T_values,
    n_values,
    xerr=T_uncertainties,
    yerr=n_uncertainties,
    fmt='o',
    label='Experimental Data',
    color='blue',
    capsize=3
)
ax1.plot(
    T_fine,
    fitted_n_nonlinear,
    label=f'Nonlinear Fit:Eg={Eg_fit:.3f}± {Eg_uncertainty:.3f}: eV,Reduced χ² = {reduced_chi_squared:.2f}',
    color='red',
    linestyle='--'
)
ax1.set_xlabel('Temperature (K)')
ax1.set_ylabel('Carrier Concentration (cm$^{-3}$)')
ax1.set_title('Carrier Concentration vs Temperature')
ax1.legend(loc='upper left')


# Residuals plot for nonlinear fit
ax2 = fig.add_subplot(gs[1])
ax2.errorbar(
    T_values,
    nonlinear_residuals,
    yerr=n_uncertainties,
    fmt='o',
    color='blue',
    capsize=3
)
ax2.axhline(0., linestyle='--', color='gray')
ax2.set_xlabel('Temperature (K)')
ax2.set_ylabel('Residuals (cm$^{-3}$)')
ax2.set_title('Residuals: Nonlinear Fit')


plt.tight_layout()
plt.show()

# Print fitting parameters and uncertainties
print(f"Fitting Parameters:")
print(f"A: {A_fit:.7e} ± {A_uncertainty:.6e}")
print(f"Eg: {Eg_fit:.4f} ± {Eg_uncertainty:.10f} eV")
print(f"C: {C_fit:.3e} ± {C_uncertainty:.3e}")

print(f"\nGoodness of Fit:")
print(f"χ² = {chi_squared:.2f}")
print(f"Reduced χ² = {reduced_chi_squared:.2f}")
print(f"Degrees of freedom = {dof}")
print("Note: A reduced χ² ≈ 1 indicates a good fit")
