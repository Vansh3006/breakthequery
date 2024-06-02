import sqlite3 as sq3

DATABASE = 'database.db'

def execute_select(query):
    with sq3.connect(DATABASE) as connection:
        try:
            with sq3.connect(DATABASE) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                connection.commit()
            return {
                'status':'success',
                'response': rows
            }

        except Exception as e:
            # raise e
            return {
                'status':'error',
                'response': str(e)
            }


def execute_query(query):
    with sq3.connect(DATABASE) as connection:
        try:
            with sq3.connect(DATABASE) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
            return {
                'status':'success',
                'response': "done"
            }

        except Exception as e:
            return {
                'status':'error',
                'response': str(e)
            }
        

