#!/usr/bin/python3
import math
import csv

class calculation:
    
    def __init__(self):
        print ("inicialization")
        self.pi = 3.1416
        self.post = 1500
        self.data = []
        self.read_data()
        self.calculate_projection()
        self.calculate_moving()

    def read_data(self):
        with open('data.csv', mode ='r')as file:
   
            csvFile = csv.reader(file,quoting=csv.QUOTE_NONNUMERIC)
            for row in csvFile: # each row is a list
                self.data.append(row)


    def calculate_projection(self):
        

        for moment in self.data:
            #print(moment[1])
            x_err = math.sin(moment[3]*self.pi/180)*self.post
            true_x = moment[1] - x_err
            
            #print(true_x)

            y_err = math.sin(moment[4]*self.pi/180)*self.post
            true_y = moment[2] - y_err
            #print(true_y)
            projected_data = [moment[0],true_x,true_y]
            print(projected_data)
    def calculate_moving(self):
        print("")
   

def main():
    calculation()


if __name__ == "__main__":
    main()