# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 11:52:20 2024

@author: Stan Munro
"""
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

class traffic:
    """simulating over time the movement of cars in traffic, plotting the outcomes and finding the average movement speed of the cars """
    def __init__(self,n,t,d):
        self.n = n
        self.t = t 
        self.d = d
    
    
    def create_road(self):
        """creating a 1 by n array to represent the initial road layout"""
        road_1 = np.zeros([self.n])
        """creating a t by n array to represent the road over all the timesteps"""
        road = np.zeros([self.t,self.n])
        
        """using a random number less than 1 to compare to density and conclude whether theres a car in initial spot"""
        for i in range(len(road_1)):
            rd = random.random()
            if rd <= self.d: 
                road_1[i] = 1      
        road[0] = road_1
        
        return road
                
        
    def simulation(self,road):
        
        av_speeds = np.zeros(self.t - 1)
        for i in range(self.t-1):
            """used to create average speed"""
            moves = 0
            cars = 0
            for j in range(self.n):
                """using modular operator to create a wrap around road where b is place before f is place after"""
                b = (j-1)% self.n 
                f = (j+1) % self.n
                
                """iteration for each spot for each timestep and then ammends based on conditions of previous and next spot"""
                if road[i,j] == 1:
                    cars = cars + 1 
                    if road[i,f] == 1:
                        road[i+1,j] = 1
                    else:
                        road[i+1,j] = 0
                        """every time a car moves foward the moves variable is increased"""
                        moves = moves + 1 
                else:
                    if road[i,b] == 1:
                        road[i+1,j] = 1
                    else:
                        road[i+1,j] = 0
            if cars != 0:
                av_speed = moves / cars
            else: 
                av_speed = 0
            
            av_speeds[i] = av_speed
        return(road,av_speeds,av_speed)
     
    def graphing_road(self,road,av_speeds):
        
        for i in range(len(av_speeds)):
            print(f"the average speed at timestep {i+1} is {av_speeds[i]} places per unit time")
        ax = plt.axes()
        r = 0.05
        
        """each element of the completed road is iterated through and if it contains a car a patch is added to the plot"""
        for i in range(self.n):
            for j in range (self.t):
                if road[j,i] == 1:
                    ax.add_patch(Circle((i,j),r,color = "b"))
        plt.xlabel("Car Road") 
        plt.ylabel("Time")
        plt.title("Car Position vs Time in traffic")    
        plt.axis("scaled") 
        plt.show()

        y = av_speeds
        x = np.linspace(0,self.t-1,self.t-1)
        plt.plot(x,y) 
        plt.xlabel("Time") 
        plt.ylabel("Velocity")
        plt.title("Veloicty vs Time of Traffic")
        plt.show()
        
    def multiple_density_simulation(self, road_2):
        loop_status = 1 
        time = 0 
        prev_av_speed = 0 
        while loop_status == 1:
    
            moves = 0
            cars = 0
            for j in range(self.n):
                
                b = (j-1)% self.n 
                f = (j+1) % self.n
                if road_2[time,j] == 1:
                    cars = cars + 1 
                    if road_2[time,f] == 1:
                        road_2[time+1,j] = 1
                    else:
                        road_2[time+1,j] = 0
                        moves = moves + 1 
                else:
                    if road_2[time,b] == 1:
                        road_2[time+1,j] = 1
                    else:
                        road_2[time+1,j] = 0
            if cars != 0:
                av_speed = moves / cars
            else: 
                av_speed = 0
                
            time = time + 1 
            if prev_av_speed == av_speed :
                x = x + 1 
            else:
                x = 0 
            if x == 3: 
                loop_status = 0
            prev_av_speed = av_speed
            
        return(av_speed)
            

    def plot_multiple_densities(self,ss_speeds):
        y = ss_speeds
        x = np.linspace(0.2,1,100)
        plt.scatter(x,y) 
        plt.xlabel("Density of Cars")
        plt.title("Veloicty vs Density of Cars of Traffic")
        plt.ylabel("Velocity")        
        plt.show()

def main(): 
    
    n = int(input("Please input the length of the road"))
    t = int(input("Please input the amount of timesteps"))
    d = float(input("Please enter the car density"))
    
    cars = traffic(n,t,d)
    road = cars.create_road()
    road , av_speeds,final_speed = cars.simulation(road)
    cars.graphing_road(road, av_speeds)
    
    """creating range of densities and looping through the process for each density"""
    car_ds = np.linspace(0.2,1,100)
    ss_speeds = np.zeros(len(car_ds))
    for i in range(len(car_ds)):
        cars_2 = traffic(n,200,car_ds[i])
        road2 = cars_2.create_road()
        road, av_speeds,ss_speed = cars_2.simulation(road2)
        ss_speeds[i]= ss_speed
    cars_2.plot_multiple_densities(ss_speeds)
     
main()