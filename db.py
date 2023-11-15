import mysql.connector
from hash import verify_password_bcrypt
CONFIG_MYSQL_DATABASE = {
    'host': 'localhost',
    'user': 'root',
    'password': 'toor',
    'database': 'app_auth',
    'port': '3306'
}
    
def connect():
    try:
        cnx = mysql.connector.connect(
            host=CONFIG_MYSQL_DATABASE['host'],
            user=CONFIG_MYSQL_DATABASE['user'],
            password=CONFIG_MYSQL_DATABASE['password'],
            database=CONFIG_MYSQL_DATABASE['database'],
            port=CONFIG_MYSQL_DATABASE['port']
        )
        if cnx.is_connected():
            print("\nConexión exitosa a la base de datos.\n")
            return cnx
        else:
            print("No se pudo conectar a la base de datos.")
            return None
    except Exception as e:
        print(e)
        return None
    

def create_table():
    cnx = connect()
    cursor = cnx.cursor()
    SQL_COMMAND = """
        CREATE TABLE IF NOT EXISTS users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            password VARCHAR(255)
        );
    """
    cursor.execute(SQL_COMMAND)
    cnx.commit()
    cursor.close()
    cnx.close()

def init_db():
    create_table()

def register_user(user_data):
    try:
        cnx = connect()
        cursor = cnx.cursor()
        SQL_COMMAND = """
            INSERT INTO app_auth.users(name, email, password)
            VALUES(%s, %s, %s);
        """
        cursor.execute(SQL_COMMAND, user_data)
        cnx.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        cnx.close()
    
def login_user(user_data):
    cnx = connect()
    cursor = cnx.cursor()
    SQL_COMMAND = """
        SELECT email, password FROM app_auth.users
        WHERE email = %s;
    """
    cursor.execute(SQL_COMMAND, (user_data[0],))
    user = cursor.fetchone()
    print(user[1])
    password = str(user[1]).encode('utf-8')
    if not verify_password_bcrypt(user_data[1], password):
        return None 
    cursor.close()
    cnx.close()
    return user

def get_email(email):
    cnx = connect()
    cursor = cnx.cursor()
    SQL_COMMAND = """
        SELECT * FROM app_auth.users
        WHERE email = %s;
    """
    cursor.execute(SQL_COMMAND, (email,))
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    return user