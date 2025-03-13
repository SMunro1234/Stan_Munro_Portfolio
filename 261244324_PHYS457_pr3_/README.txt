Numerov Method Project
Overview
This project contains C++ code implementing the Numerov method to solve differential equations. The project includes the following files:

main_numerov.cpp

numerov.cpp

numerov.h

numerov_params.h

params.h

vector_mtx.cpp

vector_mtx.h

Prerequisites
Ensure you have the following installed on your system:

GCC (GNU Compiler Collection)

A text editor or IDE (e.g., Visual Studio Code)

Compiling and Running the Code
Using Command Prompt or Terminal
Navigate to the project directory:
Open a terminal or command prompt and navigate to the directory where your source files are located.

bash
cd path/to/your/project
Compile the code:
Use the following command to compile the code using g++:

bash
g++ main_numerov.cpp numerov.cpp vector_mtx.cpp -o numerov_test -std=c++11
Run the executable:
Run the compiled executable with the input file input_text.txt:

bash
./numerov_test input_text.txt
Output
After running the executable, two files will be generated in the project directory:

params.dat: Contains the input parameters.

output.dat: Contains the calculated y values for each x.

Plotting
For plotting, an example plot is included in the zip file. However, you are encouraged to use any plotting software you prefer (e.g., gnuplot, matplotlib, Excel) to visualize the data from output.dat.

To plot using gnuplot, you can use the following command:

bash
plot 'output.dat' w l
This will display a line plot of your data.

