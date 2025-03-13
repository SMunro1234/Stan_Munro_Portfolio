#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "derivatives.h"
#include "extremum.h"
#include "solve.h"

typedef double (*FuncPT)(double);

FuncPT ORIG_FUNC; // A common variable. Only valid within this file

double Extremum_DF(double x); // Used only within this file

// Extremum_GetExtremum finds the minimum or maximum near x_init
// This function returns the value of x where the extremum is
// The variable curvature has the value of the second derivative at the extremum
double Extremum_GetExtremum(FuncPT func, double x_init, double* curvature) {
    double x, tol, ddf;
    int count;

    ORIG_FUNC = func; // To communicate with Extremum_DF

    tol = 5e-10;  // or another appropriate small value

    // Use Solve_Newton to solve 0 = Extremum_DF(x) starting with x_init
    x = Solve_Newton(0.0, Extremum_DF, x_init, tol, &count);

    // Use Derivative_SecondD to calculate the second derivative at the extremum
    ddf = Derivative_SecondD(x, ORIG_FUNC);

    // Set curvature to the second derivative
    *curvature = ddf;

    // Return the value of x at the extremum
    return x;
}

// We are using FuncPT func -> ORIG_FUNC here because
// Solve_Newton can only take in double func(double) type of function
double Extremum_DF(double x) 
{
    // Calculate the first derivative of ORIG_FUNC using Derivative_FirstD
    return Derivative_FirstD(x, ORIG_FUNC);
}
