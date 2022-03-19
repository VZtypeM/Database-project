import pick
import sqlite3
from datetime import date

database_name = "test.db"


def add_coffee_taste(email, coffee_name, roastery_id, points, notes):
    date_today = date.today()

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute(
        """
INSERT INTO CoffeeTastes (Email, CoffeeName, RoasteryID, Points, Notes, Date)
VALUES (?, ?, ?, ?, ?, ?);""",
        (email, coffee_name, roastery_id, points, notes, date_today)
        # """
        # INSERT INTO CoffeeTastes (Email, CoffeeName, RoasteryID, Points, Notes, Date)
        # VALUES (:email,:coffeeName,:roasteryID,:points,:notes,:date);""",
        # {"email" = email, "coffeeName" = coffee_name, "roasteryID" = roastery_id, "points" = points, "notes" = notes, "date" = date},
    )

    for row in cursor.execute("SELECT * FROM CoffeeTastes"):
        print(row)

    connection.close()


def main():
    options = ["add coffee taste", "log in", "search for cofffee"]
    title = "What do you want to do?"
    selected = pick.pick(options, title)
    print(selected)
    if selected[0] == "add coffee taste":
        add_coffee_taste(
            "markus.vesetrud@gmail.com", "Vinterkaffe 2022", 1, 3, "Splendid"
        )


if __name__ == "__main__":
    main()
