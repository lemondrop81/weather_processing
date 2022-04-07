import sqlite3
import dbcm

"""
    Weather processing app
    March 30, 2022
    Description: A simple program to add to the database.
"""

class DBOperations():
    """Contains database operations"""

    def initialize_db(self):
        """Initialize the database"""
        dbcm.DBCM.initialize(self)

    def save_data(self, weather):
        """Save the data to the database"""
        try:
            dbcm.DBCM.add_data(self, weather)

            print("Data successfully saved.")
        except Exception as e:
            print("Error saving data:", e)

    def purge_data(self):
        """Purges all data from database"""
        try:
            dbcm.DBCM.remove_data(self)

            print("Data successfully removed.")
        except Exception as e:
            print("Error removing data:", e)

    def print(self):
        """Prints the data from database"""
        dbcm.DBCM.print_data(self)
            

myparser = DBOperations()

myparser.purge_data()
