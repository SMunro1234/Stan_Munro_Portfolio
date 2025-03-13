#ifndef NUMEROV_PARAMS_H
#define NUMEROV_PARAMS_H

#include "params.h"

// Define Func_1D as a pointer to functions that take a double and a DynamicVars*
// and return a double
typedef double (*Func_1D)(double, DynamicVars *);

typedef struct numerov_params {
    double x_f;  // Maximum x
    double x_i;  // Minimum x
    double y_0;  // y(x_i)
    double y_1;  // y(x_i + h)
    int nmax;    // Number of sampling points
    double h;    // Step size h = (x_f - x_i) / nmax
    Func_1D NumerovFunc_F;  // The function F in y'' = Fy
} NumerovParams;

#endif
