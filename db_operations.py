"""
    Weather processing app
    March 30, 2022
    Description: A simple program to add to the database.
"""
import sqlite3
import logging
import dbcm

class DBOperations():
    """Contains database operations"""

    def __init__(self):
        """Constructor"""
        try:
            self.cursor = 0
            self.logger = logging.getLogger(__name__)
        except Exception as exception:
            self.logger.INFO("DBOperations:initialize::", exception)



    def initialize(self):
        """Initialize the database and create the table"""
        try:
            with dbcm.DBCM("weather.sqlite") as conn:
                print("Opened database successfully.")
                try:
                    connection = conn.cursor()
                    connection.execute("""create table IF NOT EXISTS weather
                                    (id integer primary key autoincrement,
                                    sample_date text key not null,
                                    location text,
                                    min_temp real,
                                    max_temp real,
                                    avg_temp real);""")
                    conn.commit()
                    print("Table created successfully.")
                except sqlite3.Error as exception:
                    self.logger.INFO("DBOperations:initialize:connection:", exception)
        except Exception as exception:
            self.logger.INFO("DBOperations:initialize::", exception)

    def save_data(self, weather):
        """Save the data to the database"""
        try:
            with dbcm.DBCM("weather.sqlite") as conn:
                try:
                    connection = conn.cursor()
                    sql = """insert OR REPLACE into weather
                            (sample_date,location,min_temp,max_temp,avg_temp)
                            values (?,?,?,?,?)"""
                    for k, value in weather.items():
                        data = (k, 'Winnipeg, MB', value['Min'], value['Max'], value['Mean'])
                        connection.execute(sql, data)
                    conn.commit()
                    print("Added sample successfully.")
                except sqlite3.Error as exception:
                    self.logger.INFO("DBOperations:save_data:connection:", exception)
        except Exception as exception:
            self.logger.INFO("DBOperations:save_data:", exception)


    def purge_data(self):
        """Purges all data from database"""
        try:
            with dbcm.DBCM("weather.sqlite") as conn:
                connection = conn.cursor()
                connection = conn.cursor()
                try:
                    connection.execute("DELETE FROM weather")
                    conn.commit()
                except sqlite3.Error as inst:
                    print("DBOperations:purge_data:delete:", inst)
                try:
                    connection.execute("DROP TABLE IF EXISTS weather")
                    conn.commit()
                except sqlite3.Error as inst:
                    self.logger.INFO("DBOperations:purge_data:drop:", inst)
                print("Successfully removed data from database")
        except Exception as exception:
            self.logger.INFO("DBOperations:purge_data:", exception)

    def fetch_data(self, inital=0, final=0, year=0, month=0):
        """returns the data from database"""
        try:
            try:
            #Get the latest date from the database
                if inital == 0 and final == 0 and year == 0 and month == 0:
                    with dbcm.DBCM("weather.sqlite") as conn:
                        connection = conn.cursor()
                        connection.execute("SELECT MAX(sample_date) FROM weather")
                        row = connection.fetchone()
                        return row
            except sqlite3.Error as inst:
                self.logger.INFO("DBOperations:fetch_data:latest_date:", inst)

            try:
                # Get the weather data for the boxplot
                if inital != 0 and final != 0:
                    with dbcm.DBCM("weather.sqlite") as conn:
                        connection = conn.cursor()
                        connection.execute(f"select * from weather WHERE sample_date between {inital} AND {final}")
                        rows = connection.fetchall()
                        return rows
            except sqlite3.Error as inst:
                self.logger.INFO("DBOperations:fetch_data:boxplot data:", inst)

            try:
                # Get the weather data for the lineplot
                if year != 0 and month != 0:
                    with dbcm.DBCM("weather.sqlite") as conn:
                        connection = conn.cursor()
                        test = f"select * from weather WHERE sample_date LIKE '{year}-{month}%'"
                        connection.execute(test)
                        rows = connection.fetchall()
                        return rows
            except sqlite3.Error as inst:
                self.logger.INFO("DBOperations:fetch_data:lineplot data:", inst)

        except Exception as exception:
            self.logger.INFO("Error fetching data.", exception)
        