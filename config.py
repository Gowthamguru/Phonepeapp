# Import the required packages
import importlib.util
import os
import subprocess
import sys

# install the missing package
def pkg_loader():
    with open('requirements.txt', 'r') as f:
        for line in f:
            #Verify the package availability
            if importlib.util.find_spec(line) is None:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', line])

# import the environment variable
from dotenv import find_dotenv, load_dotenv
# Import Mysql Libraries
import mysql.connector
from mysql.connector import Error

# Define the connectivity

def get_connection():
    try:
        # Validated the environment variable path
        # Validate the path
        dotenv_path = find_dotenv()
        # load the path
        env_val = load_dotenv(dotenv_path)
        #Verify the env path availability
        if env_val:
            _host = os.getenv("HOST")
            _userid = os.getenv("USER_ID")
            _password = os.getenv("PASSWORD")
            _database = os.getenv("DATABASE")
            #Connect the SQL Connection
            connection = mysql.connector.connect(host=_host, user=_userid, password=_password)
            if connection.is_connected():
                cursor = connection.cursor()
                #Validate the Database availability and create database
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {_database};")
                cursor.close()
                connection.close()
                conn = mysql.connector.connect(host=_host, user=_userid, password=_password,db=_database)
                if conn.is_connected():
                    print('Connection Success')
                    cur = conn.cursor()
                    return conn, cur
    except Error as e:
        print('Connection Error',e.msg)
