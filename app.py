# app.py

import os
from dotenv import load_dotenv
from openai import OpenAI
import mysql.connector as mysql

# model to be used
# base model is gpt-4.1-nano-2025-04-14
# file-tuning file id is file-2MPUmfbVhpq2XPCcyL4sk3
model = "gpt-4.1-nano-2025-04-14"

# initializing openai and mysql connectors
# returns openai client instance mysql connector instance and mysql cursor
def init():
    # load_dotenv() # loading .env
    # client = OpenAI() # openai instance
    client = ""
    cnx = mysql.connect(
        host = "127.0.0.1",
        port = 3306,
        user = "root",
        password = "example",
        database = "cgvbot"
    ) # opening mysql connection
    cur = cnx.cursor()
    # initialize logs table if not exists
    query = """
    CREATE TABLE IF NOT EXISTS logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        request LONGTEXT,
        response LONGTEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cur.execute(query)
    return client, cnx, cur

# handling openai api calls and responses
# params are openai client instance and user's request
# returns response text output
def ask(client, request):
    # handling api errors
    try:
        response = client.responses.create(
            model = model,
            input = request
        )
        return 0, response.output_text
    except Exception as e:
        return -1, f"Erreur inattendue : {str(e)}"

# saving requests/responses in db for further purposes
# such as security and evolvability of the model
def db_save(cur, cnx, request, response):
    # building query with data
    query = """
    INSERT INTO logs (request, response)
    VALUES (%s, %s)
    """
    data = (request, response)
    # saving new log
    cur.execute(query, data)
    cnx.commit()

def main():
    # initializing
    client, cnx, cur = init()
    request = ""
    print("\033[92mChatbot MonEshop - Powered by OpenAI")
    print("Des questions sur nos CGV ? Le bot vous répondra immédiatement !\033[0m")
    # main process
    while str.lower(request) != "exit":
        # user input
        request = input("Vous >> ")
        # handling exit or empty input
        if request == "" or str.lower(request) == "exit":
            break
        # openai api call
        # exception, response = ask(client, request)
        exception = 0
        color_code = "\033[92m" if exception == 0 else "\033[31m"
        response = "Réponse blabla" if exception == 0 else "Erreur blabla"
        print("Bot >> ", color_code, response, "\033[0m")
        # mysql logging
        db_save(cur, cnx, request, response)
    cnx.close()

if __name__ == "__main__":
    main()