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

try:
    """ try/catch block for handling potential MySQL database errors """

    db = mysql.connector.connect(**config)  # connect to the movies database

    # output the connection status
    print("\n  Database user {} connected to MySQL on host {} with database {}\n".format(config["user"], config["host"],
                                                                                       config["database"]))

    cursor = db.cursor()
    cursor.execute("select * from studio")
    studios = cursor.fetchall()
    print("-- DISPLAYING Studio RECORDS --")
    for studio in studios:
        print("Studio ID: {}\n"
              "Studio Name: {}\n".format(studio[0], studio[1]))
    print()

    print("-- DISPLAYING Genre RECORDS --")
    cursor.execute("select * from genre")
    genres = cursor.fetchall()
    for genre in genres:
        print("Genre ID: {}\n"
              "Genre Name: {}\n".format(genre[0], genre[1]))
    print()

    print("-- DISPLAYING Short Film RECORDS --")
    cursor.execute("select film_name, film_runtime from film where film_runtime < 120")
    films = cursor.fetchall()
    for film in films:
        print("Film Name: {}\n"
              "Runtime: {}\n".format(film[0], film[1]))
    print()

    print("-- DISPLAYING Director RECORDS in Order --")
    cursor.execute("select film_name, film_director from film group by film_name, film_director order by film_director")
    directors = cursor.fetchall()
    for director in directors:
        print("Film Name: {}\n"
              "Director: {}".format(director[0], director[1]))

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
