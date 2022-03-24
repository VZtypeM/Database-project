import sqlite3
from datetime import date


def find_roastery_id_from_names(
    database_name: str, coffee_name: str, roastery_name: str
) -> str | None:
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT RoasteryID
        FROM Roastery JOIN RoastedCoffee USING (RoasteryID)
        WHERE CoffeeName = ? AND Roastery.name = ?;
        """,
        (coffee_name, roastery_name),
    )
    result = cursor.fetchall()
    connection.close()

    if len(result) > 1:
        print("Roastery.name and CoffeeName are not unique in the database!")
        return None
    if len(result) == 0:
        print("No matching Roastery.name and CoffeeName in the database")
        return None

    # Return roastery id
    return result[0][0]


def add_coffee_taste(
    database_name: str,
    email: str,
    coffee_name: str,
    roastery_name: str,
    points: int,
    notes: str,
) -> None:
    date_today = date.today()
    roastery_id = find_roastery_id_from_names(database_name, coffee_name, roastery_name)
    if roastery_id is None:
        print("Database not modified")
        return

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
        print("Database successfully modified")
    except sqlite3.IntegrityError as error:
        print(error)
        print("Database not modified")
    finally:
        connection.close()
