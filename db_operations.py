"""
    Weather processing app
    March 30, 2022
    Description: A simple program to add to the database.
"""
from asyncio.windows_events import NULL
from email.policy import default
import dbcm

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
                except Exception as exception:
                    print("Error creating table:", exception)
        except Exception as exception:
            print("Error opening DB:", exception)

    def save_data(self, weather):
        """Save the data to the database"""
        try:
            with dbcm.DBCM("weather.sqlite") as conn:
                connection = conn.cursor()
                sql = """insert OR REPLACE into weather
                        (sample_date,location,min_temp,max_temp,avg_temp)
                        values (?,?,?,?,?)"""
                for k, value in weather.items():
                    data = (k, 'Winnipeg, MB', value['Min'], value['Max'], value['Mean'])
                    connection.execute(sql, data)
                    print(data)
                conn.commit()
                print("Added sample successfully.")
        except Exception as exception:
            print("Error inserting sample.", exception)


    def purge_data(self):
        """Purges all data from database"""
        try:
            with dbcm.DBCM("weather.sqlite") as conn:
                connection = conn.cursor()
                connection = conn.cursor()
                connection.execute("DELETE FROM weather")
                conn.commit()
                connection.execute("DROP TABLE weather")
                conn.commit()
                print("Successfully removed data from database")
        except Exception as exception:
            print("Error removing data.", exception)

    def fetch_data(self, inital=default, final=default, year=default, month=default):
        """returns the data from database"""
        try:
           #Get the latest date from the database
            if inital == NULL and final == NULL and year == NULL and month == NULL:
                with dbcm.DBCM("weather.sqlite") as conn:
                    connection = conn.cursor()
                    connection.execute("SELECT MAX(sample_date) FROM weather")
                    row = connection.fetchone()
                    return row
            # Get the weather data for the boxplot
            if inital != NULL and final != NULL:
                with dbcm.DBCM("weather.sqlite") as conn:
                    connection = conn.cursor()
                    connection.execute(f"select * from weather WHERE sample_date BETWEEN {inital} AND {final}")
                    rows = connection.fetchall()
                    return rows
            # Get the weather data for the lineplot
            if year != NULL and month != NULL:
                with dbcm.DBCM("weather.sqlite") as conn:
                    connection = conn.cursor()
                    test = f"select * from weather WHERE sample_date LIKE '{year}-{month}%'"
                    connection.execute(test)
                    rows = connection.fetchall()
                    return rows

        except Exception as exception:
            print("Error fetching data.", exception)
        