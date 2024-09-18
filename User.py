import sqlite3
import bcrypt

# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect('user_database.sqlite')


# Function to create the users table if it doesn't exist
def create_users_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()
    add_user('user1', 'user1', 'password1'),
    add_user('user', 'Harishree', 'Hari@3107')


# Function to add a new user to the database
def add_user(username, name, password):
    if not username_exists(username):
        conn = connect_db()
        cursor = conn.cursor()
        username = username.lower()
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Store the hashed password in the database
        cursor.execute('INSERT INTO users (username, name, password) VALUES (?, ?, ?)',
                       (username, name, hashed_password))

        conn.commit()
        conn.close()
        return True
    else:
        return False


# Function to check if a username already exists
def username_exists(username):
    conn = connect_db()
    username = username.lower()
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def get_user_credentials(username):
    # Ensure the users table exists
    create_users_table()

    # Connect to the database
    conn = connect_db()
    cursor = conn.cursor()
    username = username.lower()

    # Fetch only the credentials for the specific user (username)
    cursor.execute("SELECT name, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()  # Fetch the result of the query
    conn.close()

    # If the user exists, return their credentials
    if user:
        credentials = {
            'name': user[0],
            'password': user[1]
        }
        return credentials
    else:
        # If no user is found, return None
        return None

