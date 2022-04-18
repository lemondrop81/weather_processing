"""
    Weather processing app
    March 30, 2022
    Description: A simple context manager for the database
"""
import sqlite3

class DBCM():
    """Contains database operations"""

    def __init__(self, db_name):
        """Constructor"""
        self.db_name = db_name

    def __enter__(self):
        """
        Open the database connection
        """
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the connection
        """
        self.conn.close()
