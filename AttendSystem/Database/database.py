from tkinter import *
import mysql.connector

# ======================= DATABASE CLASS ================================ #
class Database:
    def __init__(self, host, database, user, password):
        self.host = host 
        self.database = database 
        self.user = user 
        self.password = password  
        self.connection = None

    #A code to a connection to the MySQL database
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Connected to database successfully")
        except mysql.connector.Error as err:
            print(f"Failed to connect to database: {err}")
            raise err

    #Execute a single query
    def execute_query(self, query, params=None):
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query, params)
                self.connection.commit()
                cursor.close()
            except mysql.connector.Error as err:
                print(f"Error executing query: {err}")
                raise err
        else:
            print("Database connection is not established")
            raise Exception("Database connection is not established")

    #Fetch multiple rows from a query
    def fetch_data(self, query, params=None):
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query, params)
                result = cursor.fetchall()
                cursor.close()
                return result
            except mysql.connector.Error as err:
                print(f"Error fetching data: {err}")
                raise err
        else:
            print("Database connection is not established")
            raise Exception("Database connection is not established")
    
    #Fetch a single row from a query
    def fetch_one(self, query, params=None):
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query, params)
                result = cursor.fetchone()
                cursor.close()
                return result
            except mysql.connector.Error as err:
                print(f"Error fetching data: {err}")
                raise err
        else:
            print("Database connection is not established")
            raise Exception("Database connection is not established")

    #Close the database connection
    def close_connection(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")
