import pymysql
from dotenv import load_dotenv
import os
import enum

class Env_variables(enum.Enum):
    db_hostname='DB_HOSTNAME'
    db_username='DB_USERNAME'
    db_password='DB_PASSWORD'
    db_name='DB_NAME'

# Load variables from the .env file into the environment
load_dotenv()

def get_db_connection():
    return pymysql.connect(
        host=os.getenv(Env_variables.db_hostname),
        user=os.getenv(Env_variables.db_username),
        password=os.getenv(Env_variables.db_password),
        database=os.getenv(Env_variables.db_name),
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db(app):
    # This can include setup logic or migrations if needed
    pass

"""

1. for production grade applications, when they run, which file is run first in flask? and how?
2. how to manage the tokens and credentials in the app code in production grade applications?
3. for production grade applications, how the db tables are created, manually on the admin panel or in the code?
4. if in the code, then how and where? how to structure the code?
5. how to use breakpoints in vscode? and how to check the values of variables at the breakpoint and how to execute expressions?
6. what is mysql? and how is it used with flask in production grade applications, which package and how the code is structured?

"""