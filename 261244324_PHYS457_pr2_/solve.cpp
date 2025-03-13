// File: solve.cpp
#include <iostream>
#include <cstdlib>
#include <cmath>
#include "solve.h"

// Numerical derivative
double Solve_Get_Df(double (*func)(double), double x);

// Solve function self-contained. But that is not strictly necessary.

// Solve_Bisect

// Solve f(x) = nu using bisect method
// Note that count is passed by reference (that is, the pointer is passed)
// because we want to change the value of it inside Solve_Bisect
double Solve_Bisect(double nu, double (*func)(double), double x_min, double x_max, double tol, int* count) {
    double x_mid, f_max, f_min, f_mid, err;
    int count_max = 1000; // Large enough

    *count += 1; // Keep track of the number of iterations.

    if (*count > count_max) { // avoiding infinite loop
        fprintf
        (stderr, "Solve_Bisect: Done %d iterations without convergence.\n",count_max);
        fprintf(stderr, "Exiting. \n");
        exit(0);
    }

    f_max = (*func)(x_max) - nu; // Calculate f_max
    f_min = (*func)(x_min) - nu; // Calculate f_min

    if (f_max * f_min > 0.0) { // we can’t find a solution within the range
        fprintf
        (stderr, "Solution not within range.\n");
        fprintf(stderr, "Exiting. \n");
        exit(0);
    }

    x_mid = (x_min + x_max) / 2.0;
    f_mid = (*func)(x_mid) - nu;

    // Calculate the error
    if (nu != 0.0) {
        err = fabs(f_mid / nu);
    }
    else {
        err = fabs(f_mid);
    }

    // If err < tol, we have a solution and the calculation ends
    if (err < tol) return x_mid;

    if (f_mid * f_max < 0.0) { // the solution is between x_mid and x_max
        return Solve_Bisect(nu, func, x_mid, x_max, tol, count);
    }
    else if (f_min * f_mid < 0.0) { // the solution is between x_min and x_mid
        return Solve_Bisect(nu, func, x_min, x_mid, tol, count);
    }
    else { // one of the factors is zero
        if (f_mid == 0.0) return x_mid;
        else if (f_max == 0.0) return x_max;
        else return x_min;
    }
}

// Solve_Newton

// solves nu = func(x) by Newton’s method
// using x_{n+1} = x_n + (nu - f(x_n))/f’(x_n)

// Numerical derivative
// This uses f’(x) = (f(x+h) - f(x-h))/(2h) + O(h^2).
// This is given to show you how to access the function passed
// in the argument
double Solve_Get_Df(double (*func)(double), double x_old) {
    double h, df;
    if (x_old != 0.0) {
        h = x_old * 1.0E-5;
    }
    else {
        h = 1.0E-5;
    }
    // This is how one accesses the function passed to this function
    // via the function pointer (*func)
    df = (*func)(x_old + h) - (*func)(x_old - h);
    df /= 2.0 * h;
    return df;
}

// Newton’s method
// x_0 is the starting point
double Solve_Newton(double nu, double (*func)(double), double x_0, double tol, int* count) {
    double x_old, x_new, err, df;
    int count_max = 1000;

    x_old = x_0; // Initial value
    do {
        df = Solve_Get_Df(func, x_old); // Get the derivative
        if (fabs(df) < tol) { // Derivative is too small
            fprintf
            (stderr, "Derrivative too small.\n");
            fprintf(stderr, "Exiting. \n");
            exit(0);
        }

        x_new = x_old + (nu - (*func)(x_old)) / df;

        // Calculate err = |((x_new - x_old) / x_old)|
        err = fabs((x_new - x_old) / x_old);

        x_old = x_new; // Set x_old = x_new

        (*count)++; // Add 1 to *count

        if (*count == count_max) { // Too many iterations
            fprintf
            (stderr, "Solve_Bisect: Done %d iterations without convergence.\n", count_max);
            fprintf(stderr, "Exiting. \n");
            exit(0);
        }
    } while (err > tol); // while this condition is satisfied

    return x_new;
}
