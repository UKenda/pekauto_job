#!/usr/bin/python3

import math
import csv
import numpy as np

class calculation:
    
    def __init__(self):
        print ("inicialization")
        self.pi = 3.1416
        self.post = 1500
        self.data = []
        self.read_data()
        self.calculate_projection(self.data)
        

    def read_data(self):
        with open('data.csv', mode ='r')as file:
   
            csvFile = csv.reader(file,quoting=csv.QUOTE_NONNUMERIC)
            for row in csvFile: # each row is a list
                self.data.append(row)


    def calculate_projection(self,data):
        i=0
        projected_data=np.delete(data,np.s_[3:5], axis=1)
        for point in data:

            #print(point[1])
            x_err = math.sin(point[4]*self.pi/180)*self.post
            true_x = point[1] - x_err
            #print(true_x)
            y_err = math.sin(point[3]*self.pi/180)*self.post
            true_y = point[2] - y_err
            #print(true_y)
            projected_data[i] = [point[0],true_x,true_y]
            i+=1

        print("vector of base")
        print("time[s] | x[mm] | y[mm] ")
        print(projected_data)
        print("")

        self.calculate_moving(projected_data)


    def calculate_moving(self,projected_data):
        first = True
        i=0
        old_point = []
        heading = []
        for point in projected_data:
            if first :
                old_point = point
                first = False
            else:
                diff_x = old_point[1] - point[1]
                diff_y = old_point[2] - point[2]
                #print("heading: x: ",diff_x,"y: ",diff_y)
                speed = math.sqrt(diff_x ** 2 + diff_y **2)/(point[0] - old_point[0])
                #print ("speed [m/s]: ", speed/1000)
                angle = math.atan(diff_y/diff_x)
                #print("angle", angle*180/self.pi)
                old_point = point
                heading = np.append(heading,[point[0],diff_x,diff_y,angle*180/self.pi,speed/1000],axis=0)
                i+=1

        print("Vector of heading")
        print("time[s] | x[mm] | y[mm] | angle[deg] | speed[m/s]")
        print(heading)

   

def main():
    calculation()


if __name__ == "__main__":
    main()