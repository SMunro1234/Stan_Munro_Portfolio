#include <cmath>
#include <vector>
#include "numerov.h"
#include "numerov_params.h"
#include "vector_mtx.h"

// Function prototypes
void Numerov_Make_Fn(std::vector<double>& numerov_F, NumerovParams* Num_Params, DynamicVars* Dyn_Vars);
void Numerov_Advance_A_Step(double* y, int n, const std::vector<double>& numerov_F, NumerovParams* Num_Params);

void Numerov_Advance(double* y, NumerovParams* Num_Params, DynamicVars* Dyn_Vars) {
    int nmax = Num_Params->nmax;

    // Allocate memory for numerov_F using a vector
    std::vector<double> numerov_F(nmax + 1);

    // Create F[n] values based on F(x)
    Numerov_Make_Fn(numerov_F, Num_Params, Dyn_Vars);

    // Initialize y[0] and y[1]
    y[0] = Num_Params->y_0;
    y[1] = Num_Params->y_1;

    // Compute y[n] for n >= 2 using the Numerov method
    for (int n = 2; n <= nmax; ++n) {
        Numerov_Advance_A_Step(y, n, numerov_F, Num_Params);
    }
}

// Populate F[n] values based on F(x)
void Numerov_Make_Fn(std::vector<double>& numerov_F, NumerovParams* Num_Params, DynamicVars* Dyn_Vars) {
    for (int n = 0; n <= Num_Params->nmax; ++n) {
        double x_n = Num_Params->x_i + n * Num_Params->h;
        numerov_F[n] = Num_Params->NumerovFunc_F(x_n, Dyn_Vars);
    }
}

// Perform one step of the Numerov method
void Numerov_Advance_A_Step(double* y, int n, const std::vector<double>& numerov_F, NumerovParams* Num_Params) {
    double h2 = Num_Params->h * Num_Params->h;

    double term1 = 2.0 * (1.0 + 5.0 * h2 * numerov_F[n - 1] / 12.0) * y[n - 1];
    double term2 = (1.0 - h2 * numerov_F[n - 2] / 12.0) * y[n - 2];
    
    double denominator = 1.0 - h2 * numerov_F[n] / 12.0;
    
    y[n] = (term1 - term2) / denominator;
}
