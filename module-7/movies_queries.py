"""
Assignment: Movies: Table Queries (Module 7)
"""
import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

# --- 1. Database Configuration Setup ---

# Load secrets from the .env file
secrets = dotenv_values(".env")

config = {
    "user": secrets.get("USER"),
    "password": secrets.get("PASSWORD"),
    "host": secrets.get("HOST"),
    "database": secrets.get("DATABASE"),
    "raise_on_warnings": True
}

# --- 2. Database Connection and Query Execution ---

db = None  # Initialize db variable
cursor = None # Initialize cursor variable

try:
    # Connect to the movies database
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    print("\n" + "="*50)
    print("Database Connection Successful for User: {}".format(config["user"]))
    print("="*50 + "\n")


    # --- QUERY 1: Select all fields for the STUDIO table ---
    print("-" * 20)
    print("Query 1: All Fields from STUDIO Table")
    print("-" * 20)

    query1 = "SELECT studio_id, studio_name FROM studio;"
    cursor.execute(query1)
    studios = cursor.fetchall()

    # Print header
    print("Studio ID | Studio Name")
    print("----------|------------")
    for studio in studios:
        print("{:<9} | {}".format(studio[0], studio[1]))
    print("\n")


    # --- QUERY 2: Select all fields for the GENRE table ---
    print("-" * 20)
    print("Query 2: All Fields from GENRE Table")
    print("-" * 20)

    query2 = "SELECT genre_id, genre_name FROM genre;"
    cursor.execute(query2)
    genres = cursor.fetchall()

    # Print header
    print("Genre ID | Genre Name")
    print("---------|------------")
    for genre in genres:
        print("{:<8} | {}".format(genre[0], genre[1]))
    print("\n")


    # --- QUERY 3: Movie names with run time less than two hours (120 minutes) ---
    print("-" * 40)
    print("Query 3: Film Names with Runtime Less Than 120 Minutes")
    print("-" * 40)

    # Assumption: runtime is stored in minutes (as INT). 2 hours = 120 minutes.
    query3 = "SELECT film_name, film_runtime FROM film WHERE film_runtime < 120;"
    cursor.execute(query3)
    short_movies = cursor.fetchall()

    # Print header
    print("Film Name | Runtime (min)")
    print("----------|--------------")
    for movie in short_movies:
        print("{:<10}| {}".format(movie[0], movie[1]))
    print("\n")


    # --- QUERY 4: Film names and directors grouped by director ---
    print("-" * 50)
    print("Query 4: List of Films Grouped by Director")
    print("-" * 50)

    # Note: GROUP BY is not used for this type of list; the output requires retrieving all film_name and film_director pairs and then sorting them by director.
    query4 = "SELECT film_director, film_name FROM film ORDER BY film_director ASC;"
    cursor.execute(query4)
    films_by_director = cursor.fetchall()

    current_director = ""
    for film in films_by_director:
        director = film[0]
        film_name = film[1]

        if director != current_director:
            print("\nDirector: {}".format(director))
            current_director = director

        print("    - {}".format(film_name))
    print("\n")


# --- 3. Error Handling and Closure ---
except mysql.connector.Error as err:
    print("\n" + "="*50)
    print("CONNECTION ERROR:")
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist.")
    else:
        print(err)
    print("="*50)

finally:
    if cursor:
        cursor.close()
    if db and db.is_connected():
        db.close()
        print("Database connection closed.")