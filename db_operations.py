import sqlite3
import weather_processing.dbcm as DBCM

"""
    Weather processing app
    March 30, 2022
    Description: A simple program to add to the database.
"""

class DBOperations():
    """Contains database operations"""

    def initialize(self):
        """Initialize the database and create the table"""
        try:
            DBCM.initialize()
            print("Opened database successfully.")
        except Exception as e:
            print("Error opening DB:", e)
            



MyDb = DBOperations()
MyDb.initialize()