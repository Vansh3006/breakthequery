import sqlite3 as sq3
import json
import os 
import sys

db_name = 'database.db'
questions_name = 'questions.json'

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

DATABASE = os.path.join(application_path, db_name)
QUESTIONS = os.path.join(application_path, questions_name)

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
        

def get_questions():
    with open(QUESTIONS) as json_contents:
        questions = json.loads(json_contents.read())['questions']
    return questions


def check_query(question, query):
    model_answer = execute_select(question['answer_key'])['response']

    answer = execute_select(query)

    if answer['status'] != 'success':
        return {
            'executed':False,
            'match':False,
            'response':f"Error: {answer['response']}"
            }
    
    else:
        user_answer = answer['response']
        if set(user_answer) == set(model_answer):
            return {
            'executed':True,
            'match':True,
            'response':"Well done, you have successfully tackled this question!"
            }
        else:
            return {
            'executed':True,
            'match':False,
            'response':f"Given query has a valid syntax, but output is not what we are looking for."
            }



if __name__ == '__main__':
    test_query = """
    SELECT test FROM Doctor WHERE Specialization = 'Physician';
    """
    print(check_query(get_questions()[0], test_query))