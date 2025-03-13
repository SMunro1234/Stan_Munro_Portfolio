// File ReadME

/*
 * README
 *
 * Solar System Simulation
Overview
This project simulates the motion of celestial bodies in the solar system using numerical integration methods. It models the gravitational interactions between the Sun and planets, visualizes their orbits, and calculates key physical properties such as total energy and orbital periods. The simulation also explores planetary alignments and compares the accuracy of the Beeman and Euler numerical methods.

Features
Accurate Orbital Simulations: Models the motion of celestial bodies using gravitational laws.

Visualization: Animates planetary orbits in 2D space.

Energy Analysis: Calculates and plots the total energy of the system over time.

Orbital Periods: Compares calculated orbital periods with actual values.

Planetary Alignment Detection: Determines how often planets align during the simulation.

Numerical Methods Comparison: Implements both Beeman and Euler methods to compare accuracy.

Installation
Clone this repository:

bash
git clone https://github.com/yourusername/solar-system-simulation.git
cd solar-system-simulation
Install the required Python libraries:

bash
pip install numpy matplotlib
Ensure that the JSON file (Solar_Parameters_simple.json) is in the same directory as the Python script.

How to Run
Open a terminal or IDE.

Run the script:

bash
python F.-Project-V3.py
The program will automatically load parameters from Solar_Parameters_simple.json and start the simulation.

Inputs
The simulation uses a JSON file (Solar_Parameters_simple.json) to define parameters for celestial bodies, including:

Number of iterations (num_iterations)

Timestep (timestep)

Gravitational constant (grav_constant)

Properties of each body:

Name, mass, orbital radius, color, and rotational period.

Example JSON structure:

json
{
  "num_iterations": 100000,
  "timestep": 0.001,
  "grav_constant": 1.18638e-4,
  "bodies": [
    {
      "name": "sun",
      "mass": 332946.0,
      "orbital_radius": 0.0,
      "colour": "y",
      "Rotational Period": 0
    },
    ...
  ]
}
Outputs
Visualizations:
Planetary Orbits: Animated plot showing planets orbiting the Sun in real-time.

Energy vs Time: A graph comparing total energy over time for Beeman and Euler methods.

Console Outputs:
Calculated orbital periods for each planet compared to actual values.

Total energy of the system at various timesteps.

Frequency of planetary alignments during the simulation.

Code Structure
Bodies Class
Handles initialization, simulation, and analysis of celestial bodies.

Key Methods:
create_road(): Initializes celestial bodies based on JSON input.

run(): Executes the simulation and generates visualizations.

energy(): Calculates total kinetic and potential energy of the system.

allignment(): Detects planetary alignments.

Simulation Class
Defines properties and behaviors of individual celestial bodies using Beeman's method.

Key Methods:
updatePos(): Updates position using Beeman's method.

updateVel(): Updates velocity using Beeman's method.

kineticEnergy(): Calculates kinetic energy for a body.

Euler_Simulation Class (Child Class)
Implements Euler's method for position and velocity updates to compare with Beeman's method.

Results
Key Observations:
The Beeman method provides more accurate results than Euler's method for long-term simulations.

Planetary alignments occur at predictable intervals based on orbital periods.

The total energy remains relatively stable, demonstrating conservation of energy in the system.

Dependencies
This project requires Python 3.x and the following libraries:

numpy

matplotlib

Install them using pip if not already installed:

bash
pip install numpy matplotlib
Future Improvements
Extend simulations to include moons or other celestial objects.

Add support for user-defined parameters via command-line input or GUI.

Improve visualization with 3D plotting libraries like matplotlib's mplot3d or plotly.

Author
Created by Stan Munro
📧 StanMunro1234@gmail.com