import pick
import sqlite3
import add_coffee_taste


def log_in(database_name: str, user_email: str):
    # The user_email argument is the user that is allready logged in
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
        return user_email

    # Return the email of the new user
    return result[0][0]


def log_out(database_name: str, user_email: str):
    return None


def add_coffee_taste_handler(database_name: str, user_email: str):
    if user_email is None:
        print("You are not logged in, please log in first")
        return
    coffee_name = input("Enter the name of the coffee you tasted")
    roastery_name = input(
        "Enter the name of the roastery where your coffee was roasted"
    )
    points = int(input("Enter the number of points you would give the coffee (0-10)"))
    notes = input("Write down any notes about the coffee")

    add_coffee_taste.add_coffee_taste(
        database_name=database_name,
        email=user_email,
        coffee_name=coffee_name,
        roastery_name=roastery_name,
        points=points,
        notes=notes,
    )


def main():
    database_name = "test.db"
    user_email = None
    options = [
        {
            "label": "Log in",
            "confirmation_message": "Logging in",
            "handler": log_in,
            "returns_email": True,
        },
        {
            "label": "Log out",
            "confirmation_message": "Logging out",
            "handler": log_out,
            "returns_email": True,
        },
        {
            "label": "Add coffee taste",
            "confirmation_message": "Adding a coffee taste",
            "handler": add_coffee_taste_handler,
            "returns_email": False,
        },
    ]

    title = "What do you want to do?"
    selected = pick.pick(
        options, title, options_map_func=lambda option: option.get("label")
    )

    print(selected[0]["confirmation_message"])
    # Run the handler function you selected
    if selected[0]["returns_email"]:
        user_email = selected[0]["handler"](database_name, user_email)
    else:
        selected[0]["handler"](database_name, user_email)


if __name__ == "__main__":
    main()
