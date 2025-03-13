# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 16:24:05 2024

@author: Stan Munro
"""
import json
import math
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from numpy.linalg import norm

class Bodies():
    
    def __init__(self):
        
        """information for solar system planets and sun imported from a JSON file"""
        with open("Solar_Parameters_simple.json") as f: 
            Solar_Parameters = json.load(f)
            
        self.niter = int(Solar_Parameters['num_iterations'])
        self.dt = float(Solar_Parameters["timestep"])
        self.G = float(Solar_Parameters["grav_constant"])
        """Finding the time in Earth years of the final timestep, used to find when to plot final graphs"""
        self.maxtime = self.niter * self.dt
        
        """Array used to store Solar System Objects that run the Beaman Integration method for Simulation"""
        self.bodies = []
        """Array used to store Solar System objects that run the Euler method for experiment 2 Simulation"""
        self.euler_b = []
        
        for body in Solar_Parameters["bodies"]:
            name = body["name"]
            mass = body["mass"]
            orbit = body["orbital_radius"]
            c = body["colour"]
            """rot stores the actual orbital time period of each planet found on the NASA website"""
            rot = body["Rotational Period"]
            """creating instances that run Beaman Simulation"""
            self.bodies.append(Simulation(name, mass, orbit, c,rot))
            """creating instances that run the Euler Simulation child class for experiment 2 """
            self.euler_b.append(Euler_Simulation(name, mass, orbit, c,rot))
            """Variable to keep a count of how many times the planets have alligned for experiment 4"""
            self.num_a = 0
        
        """Time_periods used to store the Time Periods for each Planet"""
        self.time_periods = []
        """Total_energies used to store the total Energy of the solar system at different times"""
        self.total_energies = []
        """Times used to store the times at which the Total Energy of the solar system is found in order to plot graphs"""
        self.times = []
        """Euler_energies used to store the total energy of the Solar system at different times with velocities and positions found from the Euler Method"""
        self.Euler_energies = []
        
        """set initial positions and velocities relative to sun for both Beaman Method and Euler Method"""
        """sun must be first element in bodies list"""
        for i in range(0, len(self.bodies)):
            self.bodies[i].initialise(self.G, self.bodies[0])
            self.euler_b[i].initialise(self.G, self.euler_b[0])
            
        """Finding the Initial total Energy of the system"""
        """need to convert from earth masses AU^2 yr^-2 to kg m^2 s-2 (J)
        1 earth mass = 5.97219e24 kg
        1 AU = 1.496e+11 m"""
        c =(5.97219e+24*1.496e+11*1.496e+11)/(3.154e+7*3.154e+7)
        """energy method in Bodies class finds the total Energy for both the Beaman and Euler Method systems"""
        energy,energy_e = self.energy()
        energy = energy*c
        energy_e = energy_e*c
        """adds the energy values and the time at which they were found to the arrays used to plot a graph"""
        self.total_energies.append(energy)
        self.Euler_energies.append(energy_e)
        self.times.append(0)
        """Setting the initial value for the timestep at which planetary alignment has occured to zero for experiment 4"""
        self.initilialise_alignment()

        
    def init(self):
        """initialiser for animator"""
        return self.patches

    def animate(self, i):
        """keep track of time in earth years"""
        time = (i+1)*self.dt

        """update positions for each body"""
        for j in range(0, len(self.bodies)):
            self.bodies[j].updatePos(self.G, self.dt)
            self.patches[j].center = self.bodies[j].r
            """update positions for each body Euler Method"""
            self.euler_b[j].updatePos_1(self.G, self.dt)
        
        
        
        """Update velocities. Double Loop iterates for each planet and then for each other planet"""
        for j in range(0, len(self.bodies)):
            for k in range(0, len(self.bodies)):
                if j != k:
                    """updates velocity and acceleration for body J for all other ks"""
                    self.bodies[j].updateVel(self.G, self.dt, self.bodies[k])
                    """updates velocity and acceleration for body J for all other ks:Euler Simulation"""
                    self.euler_b[j].updateVel_1(self.G, self.dt, self.euler_b[k])
        
        """Finding the total Energy of the system at each timestep, same process as finding the Intial Energy"""
        c =(5.97219e+24*1.496e+11*1.496e+11)/(3.154e+7*3.154e+7)
        energy,energy_e = self.energy()
        energy = energy*c
        energy_e = energy_e*c
        self.total_energies.append(energy)
        self.Euler_energies.append(energy_e)
        self.times.append(time)
        
        """check year and print year if new year for any planet,but only for the planets first new year"""
        for j in range(0, len(self.bodies)):
            if self.bodies[j].newYear() == True:
                if self.bodies[j].year == 1:
                    """For experiment 1 a statement comparing the calculated and the actual time period of each planet is added to self.time_periods"""
                    self.time_periods.append([f"The calculated orbital time period for {self.bodies[j].name} is {time} earth years whilst the actual time period is {self.bodies[j].rot} earth years"])
                    print (f"{self.bodies[j].name.strip()} "
                           f"{self.bodies[j].year} years = {time} earth years.")

                """if new year is earth year, also print total energy of the system"""
                if self.bodies[j].name.strip() == "earth":
                    print(f"Time = {time} earth years. "
                          f"Total energy = {energy:.3e} J.")
                               
        """Checking planetary alignment for experiment 4 at each timestep after the first 100 timesteps"""      
        if i > 100:
            i_c =i
            self.allignment(i_c)
        
        """At the Final time-step plot Total Energy Vs Time for both Methods, print the result of the time-period experiment and the number of times the planets alligned"""          
        if time == self.maxtime:
            
            plt.figure()
            Y1 = self.total_energies
            X1 = self.times   
            Y2 = self.Euler_energies
            plt.plot(X1,Y1,label = "Beaman Method")
            plt.plot(X1,Y2,label = "Euler Method")
            plt.title("Total Energy of ther Solar System vs Time")
            plt.xlabel("Time (Earth Years^-1)")
            plt.ylabel("Total Energy(J)") 
            plt.legend(loc = "upper right")
            plt.show()
            
            print(self.time_periods)
            if self.num_a != 0:
                alignment_frequency = time/self.num_a
                print(f"The planets have aligned {self.num_a} times in a period of {time} earth years."
                      f"This means that the planets align every {alignment_frequency} years")
            else: 
                print(f"The planets have not aligned in {time} earth years")
            
        return self.patches
    
    """Method to find both the total energy of the system for each simulation method"""
    def energy(self):
        
        ke = 0.0
        pe = 0.0
        for j in range(0, len(self.bodies)):
            ke += self.bodies[j].kineticEnergy()
            for k in range(0, len(self.bodies)):
                if k != j:
                    r = norm(self.bodies[k].r - self.bodies[j].r)
                    pe -= self.G*self.bodies[j].m*self.bodies[k].m / r
        """divide pe by two to avoid double countin"""
        pe = pe / 2
        totEnergy = ke + pe
    
        """Finding the energy for the Euler instances"""
        ke = 0.0
        pe = 0.0
        for j in range(0, len(self.euler_b)):
            ke += self.euler_b[j].kineticEnergy()
            for k in range(0, len(self.euler_b)):
                if k != j:
                    r = norm(self.euler_b[k].r - self.euler_b[j].r)
                    pe -= self.G*self.euler_b[j].m*self.euler_b[k].m / r
        """divide pe by two to avoid double countin"""
        pe = pe / 2
        totEnergy_e = ke + pe

        return totEnergy,totEnergy_e
    
    def initilialise_alignment(self):
        """initialse the variable self.i_a which stores the time at which the last allignment occured"""
        self.i_a = 0
     
    """method finds the angle of each planet relative to the sun and"""
    def allignment(self,i_c):
         
        angles = []
        
        for j in range(1,len(self.bodies)):
            """finding the position of the planets relative to the sun"""
            pos = self.bodies[j].r -self.bodies[0].r
            x = pos[0]
            y = pos[1]
            """using trig to find the angle from the x and y components of position adjusted for each quadrant and when x = 0"""
            if x > 0:
                if y>= 0:
                    ang = np.arctan2(y,x)
                else:
                    ang = np.arctan2(y,x)+(2*math.pi)
            elif x == 0:
                if y>0:
                    ang = math.pi/2
                else:
                    ang = 3*math.pi/2
            else: 
                if y>=0:
                    ang = np.arctan2(y,x) 
                else:
                    ang = np.arctan2(y,x) + 2*math.pi
            angles.append(ang*180/(math.pi))
        """comparing the maximum and minimum to the average angle to check whether they are within the chosen value selected to signify alignment"""   
        av_angle = sum(angles)/len(angles)
        
        """as the timestep is small and to not overcount a single allignment i_c and i_a are compared"""
        if i_c - self.i_a >50:
            if max(angles) - av_angle <= 10:
                if av_angle - min(angles) <= 10:
                    print("Planets have aligned!")
                    self.num_a = self.num_a + 1
                    """setting the current timestep to the last timestep of allignment"""
                    self.i_a = i_c 
                           
    def run(self):

        """set up the plot components"""       
        fig = plt.figure()
        ax = plt.axes()

        """create an array for patches (planets and sun)"""
        self.patches = []

        """get orbital radius of outermost planet to set size of
        orbiting bodies and of plot"""
        maxOrb = math.sqrt(np.dot(self.bodies[-1].r, self.bodies[-1].r))

        """add the planets and sun to the Axes and patches"""
        for i in range(0, len(self.bodies)):
            if i == 0:
                self.patches.append(
                    ax.add_patch(plt.Circle(self.bodies[i].r, 0.05*maxOrb,
                                            color=self.bodies[i].c, animated=True)))
            else:
                self.patches.append(
                    ax.add_patch(plt.Circle(self.bodies[i].r, 0.02*maxOrb,
                                            color=self.bodies[i].c, animated=True)))

        """set up the axes scale axes so circle looks like a circle and set limits with border b for prettier plot"""

        b = 1.2
        lim = maxOrb*b
        ax.axis("scaled")
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        plt.title("The Simulation of the Solar System")
        plt.xlabel("Distance (AU)")
        plt.ylabel("Distance(AU)") 

        self.anim = FuncAnimation(fig, self.animate, init_func=self.init, frames=self.niter, repeat=False, interval=0.0001, blit=True)
        plt.show()
       
class Simulation():
    """Planet class"""
    def __init__(self, name, mass, orbit, colour,rot):
        self.name = name
        """mass in Earth Masses"""
        self.m = mass
        """orbital radius in AU"""
        self.orbit = orbit 
        """strip removes leading or trailing white spaces"""
        self.c = colour.strip()
        self.year = 0
        self.rot = rot

    def initialise(self, G, p):
        """inital position, initial coords = (orbit radius, 0)"""
        self.r = np.array([self.orbit, 0])
        """inital velocity, tangential to position
        speed = sqrt(G*mass/r)"""
        """If the body is the sun and has a postion of (0,0) v and a = 0"""
        if self.orbit == 0.0:
            self.v = np.array([0, 0])
        else:
            vel = math.sqrt(G*p.m/self.orbit)
            self.v = np.array([0, vel])
        """intial accelatation, using gravitational force law"""
        if self.orbit == 0.0:
            self.a = np.array([0, 0])
        else:
            self.a = self.updateAcc(G, p)
        """set acc_old = acc to start Beeman or Euler for next step"""
        self.a_old = self.a

    def updatePos(self, G, dt):
        """keep old position to check for year"""
        self.r_old = self.r
        
        """update position first: Beeman Method"""
        self.r = self.r + self.v*dt + (4*self.a - self.a_old)*dt*dt/6.0
        
    def updateVel(self, G, dt, p):
        """update velocity second: Beeman
        p being the other planet e.g. p.m is the mass of the other planet"""
        a_new = self.updateAcc(G, p)
        self.v = self.v + (2*a_new + 5*self.a - self.a_old)*dt/6.0
        """now update acc ready for next iteration"""
        self.a_old = self.a
        self.a = a_new

    def updateAcc(self, G, p):
        """update acc (gravitational force law)"""
        pos = self.r - p.r
        """Acceleration given by gravitational force law"""
        a = -G*p.m*pos/(norm(pos)**3)
        return a

    def newYear(self):
        """update the year when the planet passes the +x axis"""
        if self.r_old[1] < 0.0 and self.r[1] >= 0.0:
            self.year +=1
            return True
        else:
            return False

    """determine KE"""
    def kineticEnergy(self):
        """Energy not in Joules units"""
        ke = (np.dot(self.v, self.v))*self.m/2
        return ke

"""daughter class of simulation used to run the Euler Simulation, inherits all of the methods from simulation but uses the Euler method to update position and velocity"""
class Euler_Simulation(Simulation):
    
    """the init method is taken from the Simulation class"""
    def __init__(self, name, mass, orbit, colour,rot): 
        super().__init__(name, mass, orbit, colour,rot)
    
    """Methods below are used for the Euler Method that are different from the Beaman method"""
    def updatePos_1(self, G, dt):
        self.r_old = self.r
        
        """update position first: Euler Method"""
        self.r = self.r + (self.v*dt)
        
    def updateVel_1(self, G, dt, p):
        """update velocity second: Euler Method"""
        a_new = self.updateAcc(G, p)
        self.v = self.v + (self.a*dt)
        self.a_old = self.a
        self.a = a_new
                       
def main():
    s = Bodies()
    s.run()   
main()
    