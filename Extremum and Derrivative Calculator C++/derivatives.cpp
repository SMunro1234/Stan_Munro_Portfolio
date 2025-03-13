// File derivatives.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "derivatives.h"

double Derivative_FirstD(double x, double (*func)(double)) {
    double df, h;
    h = 1.0E-5;
    if (x != 0.0) h = h * x;
    df = (func(x + h) - func(x - h)) / (2 * h);
    return df;
}

double Derivative_SecondD(double x, double (*func)(double)) {
    double ddf, h;
    h = 1.0E-5;
    if (x != 0.0) h = h * x;
    ddf = (func(x + h) + func(x - h) - 2 * func(x)) / (h * h);
    return ddf;
}
