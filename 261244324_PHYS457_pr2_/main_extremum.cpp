#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "extremum.h"

double test_func(double x);

int main(void) {
    double x_extremum, curvature, x_init;
    FILE *output;

    // Test 1
    x_init = 0.0; // Initial guess for the extremum
    x_extremum = Extremum_GetExtremum(test_func, x_init, &curvature);
    printf("Test 1: x_extremum = %e, f(x_extremum) = %e, curvature = %e\n", x_extremum, test_func(x_extremum), curvature);

    // Test 2 (uncomment to use)
    //x_init = 1.0; // Change initial guess as needed
    //x_extremum = Extremum_GetExtremum(test_func, x_init, &curvature);
    //printf("Test 2: x_extremum = %e, f(x_extremum) = %e, curvature = %e\n", x_extremum, test_func(x_extremum), curvature);

    // Test 3 (uncomment to use)
    //x_init = 4.0; // Change initial guess as needed
    //x_extremum = Extremum_GetExtremum(test_func, x_init, &curvature);
    //printf("Test 3: x_extremum = %e, f(x_extremum) = %e, curvature = %e\n", x_extremum, test_func(x_extremum), curvature);

    output = fopen("Extremum_test.dat","w");
    fprintf(output, "Results:\n");
    fprintf(output, "x_extremum = %e, f(x_extremum) = %e, curvature = %e\n\n",x_extremum, test_func(x_extremum), curvature);
    fclose(output);

    return 0;
}

double test_func(double x) {
    double f;

    // Uncomment for test 1
    f = x * x - 2.0 * x + 1;
    // This is (x-1)^2 which has the minimum at x = 1

    // Uncomment for test 2
    // f = 1.0/x/x - 2.0/x;
    // Here, assume x > 0
    // You should not set x_init = 0.0 which is a singular point.
    // A good way to guess x_init is to plot the function

    // Uncomment for test 3
    // f = 1.0/x/x - 1.0/(1.0 + exp(x - 5.0));
    // Assume x > 0
    // You should not set x_init = 0.0 which is a singular point.
    // A good way to guess x_init is to plot the function

    return f;
}
