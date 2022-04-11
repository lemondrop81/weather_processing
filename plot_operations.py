import matplotlib.pyplot as plt
import numpy as np

"""
    Weather processing app
    April 8, 2022
    Description: A simple program to add to the database.
"""

class PlotOperations():
    """Contains the code for plotting"""
    
    def boxplot(self, weather):
        """create the box plot"""
        meanTemp = []
        newList = []
        for x in weather:

           words = x[1]
           month = words.split('-')
           newList.append(int(month[1]))
           meanTemp.append(x[5])
        
        groups = [[] for i in range(max(newList))]
        [groups[newList[i]-1].append(meanTemp[i]) for i in range(len(meanTemp))]
        fig = plt.figure()
        ax  = fig.add_subplot(111)   # define the axis
        ax.boxplot(groups)
        ax.set_title('Monthly Temperature Distribution')
        ax.set_xlabel('Month')
        ax.set_ylabel('Temperature (Celsius)')
        plt.show()