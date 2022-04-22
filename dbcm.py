"""
    Weather processing app
    March 30, 2022
    Description: A simple context manager for the database
"""
import sqlite3
import logging

class DBCM():
    """Contains database operations"""

    def __init__(self, db_name):
        """Constructor"""
        try:
            self.db_name = db_name
            self.logger = logging.getLogger(__name__)
            self.conn = ""
        except Exception as inst:
            self.logger.INFO(inst)

    def __enter__(self):
        """Open the database connection"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            return self.conn
        except Exception as inst:
            self.logger.INFO(inst)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the connection"""
        try:
            self.conn.close()
        except Exception as inst:
            self.logger.INFO(inst)
