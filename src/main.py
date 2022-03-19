import pick
import sqlite3
import add_coffee_taste
from datetime import datetime

database_name = "test.db"
user_email = None


def log_in():
    # The user_email global variable is the user that is already logged in
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT email FROM User WHERE email = ? AND password = ?;", (email, password)
    )
    result = cursor.fetchall()
    connection.close()

    if len(result) == 0:
        print("No user with a matching email and password")
        # Keep the previous user logged in
        return

    # Set the email of the new user
    user_email = result[0][0]


def log_out():
    pass


# User story 1
def add_coffee_taste_handler():
    if user_email is None:
        print("You are not logged in, please log in first: ")
        return
    coffee_name = input("Enter the name of the coffee you tasted: ")
    roastery_name = input(
        "Enter the name of the roastery where your coffee was roasted: "
    )

    points = int(input("Enter the number of points you would give the coffee (0-10): "))
    notes = input("Write down any notes about the coffee: ")

    add_coffee_taste.add_coffee_taste(
        database_name=database_name,
        email=user_email,
        coffee_name=coffee_name,
        roastery_name=roastery_name,
        points=points,
        notes=notes,
    )


# User story 2
def print_users_with_coffee_tastes():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    year = datetime.now().year
    year = f"{year}-01-01"

    print("\nFullName: CoffesDrunk")
    for row in cursor.execute(
        """
        SELECT DISTINCT FullName, COUNT(*) as CoffeesDrunk
        FROM CoffeeTastes JOIN Roastery USING (RoasteryID) JOIN User USING (email)
        WHERE date >= ?
        GROUP BY email
        ORDER BY CoffeesDrunk DESC;
        """,
        (year,),
    ):
        print(row[0] + ": " + str(row[1]))

    connection.close()


# User story 3
def show_coffee_value():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    print("\nRoasteryName, CoffeeName: Price=PricePerKilo, Value=Value")
    for row in cursor.execute(
        """
        SELECT Roastery.name as RoasteryName, CoffeeName, PricePerKilo, AVG(Points)/PricePerKilo as Value
        FROM Roastery JOIN RoastedCoffee USING (RoasteryID) JOIN CoffeeTastes USING (RoasteryID, CoffeeName)
        GROUP BY RoasteryID, CoffeeName
        ORDER BY Value DESC;
        """
    ):
        print(f"{row[0]}, {row[1]}: Price={row[2]}, Value={row[3]}")

    connection.close()


# User story 4
def search_description():
    search_term = input("Enter the term you want to search after: ")
    search_term = "%" + search_term + "%"

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    print("\nRoasteryName, CoffeeName")
    for row in cursor.execute(
        """
        SELECT DISTINCT Roastery.name as RoasteryName, CoffeeName
        FROM Roastery JOIN RoastedCoffee USING (RoasteryID) JOIN CoffeeTastes USING (RoasteryID, CoffeeName)
        WHERE Notes LIKE ? OR Description LIKE ?;
        """,
        (search_term, search_term),
    ):
        print(f"{row[0]}, {row[1]}")

    connection.close()


def main():
    options = [
        {
            "label": "Log in",
            "confirmation_message": "Logging in",
            "handler": log_in,
        },
        {
            "label": "Log out",
            "confirmation_message": "Logging out",
            "handler": log_out,
        },
        {
            "label": "Add coffee taste",
            "confirmation_message": "Adding a coffee taste",
            "handler": add_coffee_taste_handler,
        },
        {
            "label": "Print users who have tasted the most coffee",
            "confirmation_message": "Printing the number of coffes each user has drunk",
            "handler": print_users_with_coffee_tastes,
        },
        {
            "label": "Print the value and price of each coffee",
            "confirmation_message": "Printing coffee values",
            "handler": show_coffee_value,
        },
        {
            "label": "Search coffee descriptions",
            "confirmation_message": "Searching coffee descriptions",
            "handler": search_description,
        },
    ]

    title = "What do you want to do?"
    while True:
        selected = pick.pick(
            options, title, options_map_func=lambda option: option.get("label")
        )

        print(selected[0]["confirmation_message"])

        # Run the handler function you selected
        selected[0]["handler"]()

        feedback = input('Press enter to continue or "q" to quit: ').lower()
        if feedback == "q":
            return


if __name__ == "__main__":
    main()
