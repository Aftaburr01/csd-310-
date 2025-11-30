"""
Assignment: Movies: Update & Deletes (Module 8)
This script demonstrates database connection, CRUD operations (Insert, Update, Delete),
and custom function usage for structured output.
"""
import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

# --- 1. Database Configuration Setup ---

# Load secrets from the .env file
secrets = dotenv_values(".env")

# Note: Using .get() prevents KeyError if a field is missing, returning None instead.
config = {
    "user": secrets.get("USER"),
    "password": secrets.get("PASSWORD"),
    "host": secrets.get("HOST"),
    "database": secrets.get("DATABASE"),
    "raise_on_warnings": True
}

# --- 2. Custom Function for Display (R in CRUD) ---

def show_films(cursor, title):
    """
    Executes a complex INNER JOIN query to display film details 
    (Name, Director, Genre Name, Studio Name) and formats the output.
    """
    print("=" * 70)
    print(f"--- {title} ---")
    print("=" * 70)

    # Use multi-line SQL string (triple quotes) for readability
    query = """
    SELECT 
        f.film_name AS Name,
        f.film_director AS Director,
        g.genre_name AS Genre,
        s.studio_name AS Studio
    FROM 
        film f
    INNER JOIN 
        genre g ON f.genre_id = g.genre_id
    INNER JOIN 
        studio s ON f.studio_id = s.studio_id
    ORDER BY f.film_name;
    """

    try:
        cursor.execute(query)
        films = cursor.fetchall()

        # Print header
        print("{:<30} {:<20} {:<15} {:<15}".format("Name", "Director", "Genre", "Studio"))
        print("-" * 80)

        # Print data
        for film in films:
            print("{:<30} {:<20} {:<15} {:<15}".format(film[0], film[1], film[2], film[3]))

        print("-" * 80)

    except mysql.connector.Error as err:
        print(f"Error executing SELECT query: {err}")


# --- 3. Main Execution Block (CRUD Operations) ---

db = None
cursor = None
try:
    # Connect to the movies database
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    print("\n--- DATABASE OPERATIONS START ---")

    # Initial display
    show_films(cursor, "INITIAL DATABASE CONTENTS")


    # --- INSERT (Create) Operation ---
    # Inserting 'Inception' (Action/Sci-Fi) using existing Studio/Genre IDs
    # ASSUMPTION: Studio ID 1 (Universal), Genre ID 2 (Comedy/Action) or similar exists.
    # To make this robust, we should SELECT the IDs, but for this assignment, we use hardcoded example IDs (1 for Studio, 1 for Genre)

    # We must first get the IDs for our new film's relationships
    # Assuming Universal Studio (ID 1) and Action Genre (ID 1) exist.
    # Replace these IDs if your setup is different.
    NEW_FILM_STUDIO_ID = 1  
    NEW_FILM_GENRE_ID = 1  

    insert_query = """
    INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
    VALUES ('Inception', '2010-07-16', 148, 'Christopher Nolan', %s, %s);
    """
    cursor.execute(insert_query, (NEW_FILM_STUDIO_ID, NEW_FILM_GENRE_ID))
    db.commit()
    print(f"\n[INFO] Successfully inserted 1 record: Inception")

    # Display films after INSERT
    show_films(cursor, "DATABASE AFTER INSERTING 'INCEPTION'")


    # --- UPDATE Operation ---
    # Update 'Alien' to be a Horror film (Genre ID 3)
    # 1. Get the genre_id for 'Horror'
    cursor.execute("SELECT genre_id FROM genre WHERE genre_name = 'Horror';")
    horror_genre_id = cursor.fetchone()

    if horror_genre_id:
        update_query = """
        UPDATE film SET genre_id = %s WHERE film_name = 'Alien';
        """
        cursor.execute(update_query, (horror_genre_id[0],))
        db.commit()
        print("\n[INFO] Successfully updated 'Alien' to Horror genre.")
    else:
        print("\n[WARNING] Could not find 'Horror' genre to perform update.")

    # Display films after UPDATE
    show_films(cursor, "DATABASE AFTER UPDATING 'ALIEN' TO HORROR")


    # --- DELETE Operation ---
    # Delete the movie 'Gladiator'
    delete_query = """
    DELETE FROM film WHERE film_name = 'Gladiator';
    """
    cursor.execute(delete_query)
    db.commit()
    print("\n[INFO] Successfully deleted 'Gladiator'.")

    # Display films after DELETE
    show_films(cursor, "DATABASE AFTER DELETING 'GLADIATOR'")


    print("\n--- DATABASE OPERATIONS END ---")

except mysql.connector.Error as err:
    print("\n" + "="*70)
    print("FATAL CONNECTION/DATABASE ERROR:")
    if db and db.is_connected():
        db.rollback() # Rollback any uncommitted changes on error
        print("Transaction rolled back due to error.")
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist.")
    else:
        print(err)
    print("="*70)

finally:
    if cursor:
        cursor.close()
    if db and db.is_connected():
        db.close()
        print("Database connection closed.")