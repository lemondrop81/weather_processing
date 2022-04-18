"""
    Weather processing app
    April 8, 2022
    Description: A simple program to add to the database.
"""
import matplotlib.pyplot as plt

class PlotOperations():
    """Contains the code for plotting"""

    def boxplot(self, weather, initial_year, final_year):
        """create the box plot"""
        mean_temp = []
        new_list = []
        for current_temp in weather:
            words = current_temp[1]
            month = words.split('-')
            new_list.append(int(month[1]))
            mean_temp.append(current_temp[5])
        groups = [[] for i in range(max(new_list))]
        [groups[new_list[i]-1].append(mean_temp[i]) for i in range(len(mean_temp))]
        fig = plt.figure()
        ax  = fig.add_subplot(111)   # define the axis
        ax.boxplot(groups)
        ax.set_title(f'Monthly Temperature Distribution for: {initial_year} to {final_year}')
        ax.set_xlabel('Month')
        ax.set_ylabel('Temperature (Celsius)')
        plt.show()

    def lineplot(self, weather):
        """create the line plot"""
        mean_temp = []
        date = []
        for current_temp in weather:
            words = current_temp[1]
            date.append(words)
            mean_temp.append(current_temp[5])
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
