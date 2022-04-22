"""
    Weather processing app
    April 8, 2022
    Description: A simple program to add to the database.
"""
import matplotlib.pyplot as plt
import logging

class PlotOperations():
    """Contains the code for plotting"""

    def __init__(self):
        """Constructor"""

    def boxplot(self, weather, initial_year, final_year):
        """create the box plot"""
        try:
            self.logger = logging.getLogger('PlotOperations:boxplot')
            mean_temp = []
            box_weather = []
            try:
                for current_temp in weather:
                    words = current_temp[1]
                    month = words.split('-')
                    box_weather.append(int(month[1]))
                    mean_temp.append(current_temp[5])
            except ValueError as error:
                self.logger.error('PlotOperations:boxplot:for', error)
            groups = [[] for i in range(max(box_weather))]
            [groups[box_weather[i]-1].append(mean_temp[i]) for i in range(len(mean_temp))]
            fig = plt.figure()
            ax  = fig.add_subplot(111)   # define the axis
            ax.boxplot(groups)
            ax.set_title(f'Monthly Temperature Distribution for: {initial_year} to {final_year}')
            ax.set_xlabel('Month')
            ax.set_ylabel('Temperature (Celsius)')
            plt.show()
        except Exception as error:
            self.logger.INFO('PlotOperations:boxplot', error)

    def lineplot(self, weather):
        """create the line plot"""
        try:
            self.logger = logging.getLogger('PlotOperations:lineplot')
            mean_temp = []
            date = []
            try:
                for current_temp in weather:
                    words = current_temp[1]
                    date.append(words)
                    mean_temp.append(current_temp[5])
            except ValueError as error:
                self.logger.error('PlotOperations:lineplot')
            fig = plt.figure()
            ax  = fig.add_subplot(111)   # define the axis
            ax.set_title('Daily Avg Temperatures')
            ax.set_xlabel('Day of Month')
            ax.set_ylabel('Average Daily Temp')

            # automaticall set font and rotation for date tick labels
            plt.gcf().autofmt_xdate()
            plt.grid(True)
            plt.plot(date, mean_temp)
            plt.show()
        except Exception as error:
            self.logger.INFO('PlotOperations:lineplot', error)
