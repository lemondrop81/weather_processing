import sqlite3
import dbcm
import plot_operations

"""
    Weather processing app
    March 30, 2022
    Description: A simple program to add to the database.
"""

class DBOperations():
    """Contains database operations"""

    def __init__(self):
        """Constructor"""
        self.cursor = 0

    def initialize(self):
        """Initialize the database and create the table"""
        try:
            with dbcm.DBCM("weather.sqlite") as conn:
                print("Opened database successfully.")
                try:    
                    c = conn.cursor()
                    c.execute("""create table IF NOT EXISTS weather 
                                    (id integer primary key autoincrement,
                                    sample_date text key not null,
                                    location text,
                                    min_temp real,
                                    max_temp real,
                                    avg_temp real);""")
                    conn.commit()
                    print("Table created successfully.")
                except Exception as e:
                    print("Error creating table:", e)
        except Exception as e:
            print("Error opening DB:", e)

    def save_data(self, weather):
        """Save the data to the database"""
        try:
            with dbcm.DBCM("weather.sqlite") as conn:
                c = conn.cursor()
                sql = """insert OR REPLACE into weather (sample_date,location,min_temp,max_temp,avg_temp)
                        values (?,?,?,?,?)"""
                for k, v in weather.items():
                    data = (k, 'Winnipeg, MB', v['Min'], v['Max'], v['Mean'])
                    c.execute(sql, data)
                    print(data)
                conn.commit()
                print("Added sample successfully.")
        except Exception as e:
            print("Error inserting sample.", e)


    def purge_data(self):
        """Purges all data from database"""
        try:
            with dbcm.DBCM("weather.sqlite") as conn:
                c = conn.cursor()
                c = conn.cursor()
                c.execute("DELETE FROM weather")
                conn.commit()
                c.execute("DROP TABLE weather")
                conn.commit()
                print("Successfully removed data from database")
        except Exception as e:
            print("Error removing data.", e)

    def fetch_data(self):
        """returns the data from database"""
        try:
            with dbcm.DBCM("weather.sqlite") as conn:
                c = conn.cursor()
                c.execute("select * from weather")
                rows = c.fetchall()
                plot_operations.PlotOperations.lineplot(self, rows)
                return rows
        except Exception as e:
            print("Error fetching data.", e)
            

myparser = DBOperations()

myparser.fetch_data()
