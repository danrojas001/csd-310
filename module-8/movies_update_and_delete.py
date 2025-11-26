""" import statements """
import mysql.connector  # to connect
from mysql.connector import errorcode

# import dotenv  # to use .env file
from dotenv import dotenv_values

# using our .env file
secrets = dotenv_values(".env")

""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}  # not in .env file


def main():
    try:
        db = mysql.connector.connect(**config)  # connect to the movies database

        # output the connection status
        print("\n  Database user {} connected to MySQL on host {} with database {}\n".format(config["user"],
                                                                                             config["host"],
                                                                                             config["database"]))

        cursor = db.cursor()
        """========================================FUNCTION CALLS HERE========================================"""
        show_films(cursor, 'DISPLAYING FILMS')
        insert_film(cursor)  # insert Jurrasic Park
        show_films(cursor, 'DISPLAYING FILMS AFTER INSERT')
        update_film(cursor)  # update Alien
        show_films(cursor, 'DISPLAYING FILMS AFTER UPDATE- Changed Alien to Horror')
        delete_film(cursor)  # delete Gladiator
        show_films(cursor, 'DISPLAYING FILMS AFTER DELETE')
        """========================================FUNCTION CALLS HERE========================================"""

        input("\n\n  Press any key to continue...")
    except mysql.connector.Error as err:
        """ on error code """
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("  The supplied username or password are invalid")

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("  The specified database does not exist")

        else:
            print(err)
    finally:
        """ close the connection to MySQL """
        db.close()


"""========================================USED FUNCTIONS HERE========================================"""
def show_films(cursor, title):
    cursor.execute("select film_name as Name, film_director as Director, genre_name as Genre, studio_name as "
                   "'Studio Name' from film inner join genre on film.genre_id = genre.genre_id inner join studio "
                   "on film.studio_id = studio.studio_id order by film_id")
    films = cursor.fetchall()
    print("\n -- {} --".format(title))
    for film in films:
        print("Film Name: {}\n"
              "Director: {}\n"
              "Genre Name ID: {}\n"
              "Studio Name: {}\n".format(film[0], film[1], film[2], film[3]))


def insert_film(cursor):
    cursor.execute("insert into film (film_name, film_releaseDate, film_runtime, film_director, studio_id, "
                   "genre_id) values ('Jurrasic Park', 1993, 127, 'Steven Spielberg', 3, 2)")


def update_film(cursor):
    cursor.execute("update film set genre_id = 1 where film_id = 2")


def delete_film(cursor):
    cursor.execute("delete from film where film_id = 1")
"""========================================USED FUNCTIONS HERE========================================"""

if __name__ == "__main__":
    main()
