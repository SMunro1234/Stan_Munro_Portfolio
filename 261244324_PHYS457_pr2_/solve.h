// File: solve.h
// Author: STAN MUNRO
#ifndef SOLVE_H
#define SOLVE_H

// Solve_Bisect solves f(x) = nu using the bisect search method
double Solve_Bisect(double nu, double (*func)(double), double x_min, double x_max, double tol, int* count);

// Solve_Newton solves f(x) = nu using Newton’s method
double Solve_Newton(double nu, double (*func)(double), double x_0, double tol, int* count);

#endif // end if
