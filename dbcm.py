import sqlite3
"""
    Weather processing app
    March 30, 2022
    Description: A simple context manager for the database
"""

class DBCM():
    """Contains database operations"""

    def initialize(self):
        """Initialize the database and create the table"""
        try:
            conn = sqlite3.connect("weather.sqlite")
            print("Opened database successfully.")
        except Exception as e:
            print("Error opening DB:", e)
        try:
            weather = {'2018-06-01': {'Max': 12.0, 'Min': 5.6, 'Mean': 7.1},
                       '2018-06-02': {'Max': 22.2, 'Min': 11.1, 'Mean': 15.5},
                       '2018-06-03': {'Max': 31.3, 'Min': 29.9, 'Mean': 30.0}}                 
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
        self.add_data(weather)

    def add_data(self, weather):
        """Adds the weather to the database"""
        try:
            conn = sqlite3.connect("weather.sqlite")
            c = conn.cursor()
            sql = """insert into weather (sample_date,location,min_temp,max_temp,avg_temp)
                    values (?,?,?,?,?)"""
            for k, v in weather.items():
                data = (k, 'Winnipeg, MB', v['Min'], v['Max'], v['Mean'])
                c.execute(sql, data)
                print(data)
            conn.commit()
            print("Added sample successfully.")
        except Exception as e:
            print("Error inserting sample.", e)
        self.print_data()

    def print_data(self):
        try:
            conn = sqlite3.connect("weather.sqlite")
            c = conn.cursor()
            for row in c.execute("select * from weather"):
                print(row)
        except Exception as e:
            print("Error fetching samples.", e)
        conn.close()

