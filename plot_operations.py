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
           newList.append(x[1])
           meanTemp.append(x[5])
        
        spread = np.random.rand(50) * 100
        center = np.ones(25) * 50
        flier_high = max(meanTemp)
        flier_low = min(meanTemp)
        data = np.concatenate((spread, center, flier_high, flier_low), 0)

        plt.boxplot(data)