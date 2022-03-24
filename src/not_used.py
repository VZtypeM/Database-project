# This file contains the unsued spesific searches mathcing user story 4 and 5
import sqlite3


# User story 4
def search_description(database_name: str):
    # Lets the user search the description of coffees by users or roasteries according to user story 4
    # This is a special case of the more generic search option we have implemented
    search_term = "%" + input("Enter the term you want to search after: ") + "%"

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    print(f"The following coffees contain the search term {search_term[1:-1]}")
    print("\nRoasteryName, CoffeeName")
    for row in cursor.execute(
        """
        SELECT DISTINCT Roastery.name as RoasteryName, CoffeeName
        FROM Roastery JOIN RoastedCoffee USING (RoasteryID) LEFT OUTER JOIN CoffeeTastes USING (RoasteryID, CoffeeName)
        WHERE Notes LIKE ? OR Description LIKE ?;
        """,
        (search_term, search_term),
    ):
        print(f"{row[0]}, {row[1]}")

    connection.close()


# User story 5
def search_country_and_method(database_name: str):
    # Lets the user search for countries and methods according to user story 5
    # This is a special case of the more generic search option we have implemented
    search_country = "%" + input("Enter the country you want to search after: ") + "%"
    search_method = (
        "%" + input("Enter the processing method you want to search after: ") + "%"
    )

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    print("\nRoasteryName, CoffeeName")
    for row in cursor.execute(
        """
        SELECT DISTINCT Roastery.name as RoasteryName, CoffeeName
        FROM Roastery 
        JOIN RoastedCoffee USING (RoasteryID) 
        JOIN CoffeeBatch USING (BatchID) 
        JOIN Farm USING (FarmID) 
        WHERE MethodName LIKE ? OR Country LIKE ?;
        """,
        (search_method, search_country),
    ):
        print(f"{row[0]}, {row[1]}")

    connection.close()
