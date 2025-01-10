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
        host='localhost',#os.getenv(Env_variables.db_hostname.value),
        user='root',#os.getenv(Env_variables.db_username.value),
        password='myssinghdbms',#os.getenv(Env_variables.db_password.value),
        database='blog_db',#os.getenv(Env_variables.db_name.value),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

#create the articles table here
conn = get_db_connection()
cursor = conn.cursor()
create_table_query = """CREATE TABLE articles (
    id INT AUTO_INCREMENT PRIMARY KEY,               
    author VARCHAR(255) NOT NULL,                    
    date_of_publishing DATE NOT NULL,                
    hashtags TEXT,                                   
    content TEXT NOT NULL                             
);"""

#cursor.execute(create_table_query)
conn.close()

def init_db(app):
    # This can include setup logic or migrations if needed
    pass

"""

for production grade applications, how the db tables are created, manually on the admin panel or in the code?
if in the code, then how and where? how to structure the code?
what is mysql? and how is it used with flask in production grade applications, which package and how the code is structured?


changes needed:
1. handle all the status codes for each api and integrate the database
2. write production quality code by dividing it into required files
3. comment the code
4. write test cases
"""