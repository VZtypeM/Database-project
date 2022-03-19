import pick
import sqlite3
from datetime import date

database_name = "test.db"


def add_coffee_taste(email, coffee_name, roastery_id, points, notes):
    date_today = date.today()

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    try:
        # Remember to turn on foreign keys
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(
            """
            INSERT INTO CoffeeTastes (Email, CoffeeName, RoasteryID, Points, Notes, Date)
            VALUES (?, ?, ?, ?, ?, ?);""",
            (email, coffee_name, roastery_id, points, notes, date_today),
        )

        connection.commit()
        connection.close()
    except sqlite3.IntegrityError as error:
        print(error)
        print("Database not modified")
        connection.close()


def main():
    options = ["add coffee taste", "log in", "search for cofffee"]
    title = "What do you want to do?"
    selected = pick.pick(options, title)
    print(selected)
    if selected[0] == "add coffee taste":
        add_coffee_taste("ola.nordman@gmail.com", "Vinterkaffe 2022", 2, 7, "Splendid")


if __name__ == "__main__":
    main()
