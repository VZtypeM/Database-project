import sqlite3
from datetime import date
from pick import pick


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

    if len(result) > 1:
        cursor.execute(
            "SELECT RoasteryID, Name, Country, Region FROM Roastery WHERE Roastery.Name = ?",
            (roastery_name,),
        )

        result = cursor.fetchall()
        connection.close()

        roastery_options = []
        for row in result:
            roastery_options.append(
                {
                    "label": f'Roastery "{row[1]}" in {row[3]}, {row[2]}',
                    "roasteryID": row[0],
                }
            )

        title = """There are several coffees in the database with the given roastery and coffee name.
Please specify which roastery you mean, by country and region."""
        selected, _ = pick(
            roastery_options, title, options_map_func=lambda option: option.get("label")
        )
        return selected["roasteryID"]

    connection.close()
    if len(result) == 0:
        print("No matching Roastery.name and CoffeeName in the database")
        return None

    # Return roastery id
    return result[0][0]


def add_coffee_taste(
    database_name: str,
    email: str,
    coffee_name: str,
    roastery_id: int,
    points: int,
    notes: str,
) -> None:
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
        print("Database successfully modified")
    except sqlite3.IntegrityError as error:
        print(error)
        print("Database not modified")
    finally:
        connection.close()
