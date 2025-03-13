#include <stdio.h>
#include <stdlib.h>
#include "vector_mtx.h"


double *vector_malloc(int nmax) {// Allocate memory space for a 1D array
    double *pt;
    int n;
    pt = (double *)malloc(sizeof(double) * nmax);// Initialize all entries to 0
    
    for (n = 0; n < nmax; n++) pt[n] = 0.0;
    return pt;
}


double **mtx_malloc(int mmax, int nmax) {// Allocate memory space for a 2D array
    double **pt;
    int m, n;
    pt = (double **)malloc(sizeof(double *) * mmax);
    for (m = 0; m < mmax; m++) {
        pt[m] = (double *)malloc(sizeof(double) * nmax);
    }
    
    for (m = 0; m < mmax; m++) {// Initialize all entries to 0
        for (n = 0; n < nmax; n++) {
            pt[m][n] = 0.0;
        }
    }
    return pt;
}


void mtx_free(double **mtx, int mmax) {// Free the memory space allocated by mtx_malloc
    int m;
    for (m = 0; m < mmax; m++) {
        free(mtx[m]);
    }
    free(mtx);
    return;
}