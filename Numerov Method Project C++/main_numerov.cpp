#include <iostream>
#include <fstream>
#include <cmath>
#include "params.h"
#include "numerov_params.h"
#include "numerov.h"
#include "vector_mtx.h"

// Function prototypes
double TestF(double x, DynamicVars* Dyn_Vars);
void ReadInNum_Params(const std::string& input_file_name, NumerovParams* Num_Params);
void PrintParams(const NumerovParams& Num_Params);
void PrintY(const double* y, const NumerovParams& Num_Params);

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <input_file>" << std::endl;
        return 1;
    }

    std::string input = argv[1];
    NumerovParams Num_Params;
    DynamicVars Dyn_Vars;

    // Read parameters from input file
    ReadInNum_Params(input, &Num_Params);
    PrintParams(Num_Params);

    // Allocate memory for the solution array
    double* y = new double[Num_Params.nmax + 1];

    // Assign the function F(x) in y'' = F(x)y
    Num_Params.NumerovFunc_F = TestF;

    // Solve using the Numerov method
    Numerov_Advance(y, &Num_Params, &Dyn_Vars);

    // Output results
    PrintY(y, Num_Params);

    // Free allocated memory
    delete[] y;

    return 0;
}

// Example function F(x) for testing (Airy equation)
double TestF(double x, DynamicVars* Dyn_Vars) {
    return -x;
}

// Read parameters from an input file
void ReadInNum_Params(const std::string& input_file_name, NumerovParams* Num_Params) {
    std::ifstream input_file(input_file_name);
    if (!input_file) {
        std::cerr << "Error opening file: " << input_file_name << std::endl;
        exit(1);
    }

    input_file >> Num_Params->x_i >> Num_Params->x_f >> Num_Params->y_0 >> Num_Params->y_1 >> Num_Params->nmax;
    Num_Params->h = (Num_Params->x_f - Num_Params->x_i) / Num_Params->nmax;

    input_file.close();
}

// Print parameters to a file for debugging
void PrintParams(const NumerovParams& Num_Params) {
    std::ofstream output("params.dat");
    if (!output) {
        std::cerr << "Error opening params.dat for writing." << std::endl;
        exit(1);
    }

    output << "x_i = " << Num_Params.x_i << "\n"
           << "x_f = " << Num_Params.x_f << "\n"
           << "y_0 = " << Num_Params.y_0 << "\n"
           << "y_1 = " << Num_Params.y_1 << "\n"
           << "nmax = " << Num_Params.nmax << "\n"
           << "h = " << Num_Params.h << std::endl;

    output.close();
}

// Print results to a file
void PrintY(const double* y, const NumerovParams& Num_Params) {
    std::ofstream output("output.dat");
    if (!output) {
        std::cerr << "Error opening output.dat for writing." << std::endl;
        exit(1);
    }

    for (int n = 0; n <= Num_Params.nmax; ++n) {
        double xn = Num_Params.x_i + n * Num_Params.h;
        output << xn << "  " << y[n] << "\n";
    }

    output.close();
}
