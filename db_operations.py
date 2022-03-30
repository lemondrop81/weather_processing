import sqlite3
import dbcm

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
            dbcm.DBCM.initialize(self)

            print("Opened database successfully.")
        except Exception as e:
            print("Error opening DB:", e)

    def purge_data(self):
        """Purges all data from database"""
            



MyDb = DBOperations()
MyDb.initialize()