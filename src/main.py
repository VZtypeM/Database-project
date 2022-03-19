import pick
import sqlite3
import add_coffee_taste
from datetime import datetime

database_name = "test.db"
user_email = None


def log_in():
    # The user_email global variable is the user that is allready logged in
    global user_email
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
    global user_email
    user_email = None


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


def print_users_with_coffee_tastes():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    year = datetime.now().year
    year = f"{year}-01-01"
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
        print(row)

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
    ]

    title = "What do you want to do?"
    while True:
        selected = pick.pick(
            options, title, options_map_func=lambda option: option.get("label")
        )

        print(selected[0]["confirmation_message"])

        # Run the handler function you selected
        selected[0]["handler"]()

        print(user_email)

        feedback = input('Press enter to continue or "q" to quit: ').lower()
        if feedback == "q":
            return


if __name__ == "__main__":
    main()
