import pymysql
import json

class Database:
    def __init__(self):
        pass

    def get_database_keys(self, path):
        with open(path, "r") as database_keys_file:
            database_keys = json.loads(database_keys_file.read())

        return database_keys

    def connect(self, database_keys):
        try:
            database = pymysql.connect(host = database_keys["host"], user = database_keys["user"], password = database_keys["password"], database = database_keys["database"])

            return database
        except Exception as database_error:
            raise Exception("Error during connecting to database - " + str(database_error))

    def database_initial_steps(self):
        database_keys = self.get_database_keys("data/database_data.json")

        database = self.connect(database_keys)
        database_cursor = database.cursor()

        return database, database_cursor

    def get_data(self, command):
        database, database_cursor = self.database_initial_steps()
        try:
            database_cursor.execute(command)
            database_response = database_cursor.fetchall()
        except Exception as database_error:
            raise Exception("Error during getting data from database - " + str(database_error))
        finally:
            database_cursor.close()
            database.close()

        return database_response

    def insert_data(self, command, values):
        database, database_cursor = self.database_initial_steps()
        try:
            database_cursor.execute(command, values)
            database.commit()
        except Exception as database_error:
            database_cursor.close()
            database.close()
            raise Exception("Error during inserting data to database - " + str(database_error))
        else:
            database_cursor.close()
            database.close()
            last_row_id = database_cursor.lastrowid

            return last_row_id

    def delete_data(self, command):
        database, database_cursor = self.database_initial_steps()
        try:
            database_cursor.execute(command)
            database.commit()
        except Exception as database_error:
            raise Exception("Error during deleting data from database - " + str(database_error))
        finally:
            database_cursor.close()
            database.close()