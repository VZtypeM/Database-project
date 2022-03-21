from pick import pick
import sqlite3
from add_coffee_taste import add_coffee_taste
from datetime import datetime
from general_search import general_search

# We know, we know, global variables are bad practice, but it makes the code easier and more readable
user_email = None


def log_in(database_name: str):
    # Asks the user to enter the email and password,
    # checks that this matches an entry in the database,
    # and logs in by setting the user_email global variable

    global user_email
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


def log_out(database_name: str):
    # Sets the global user_emal variable to None
    global user_email
    user_email = None


# def read_query(connection, query):
#     cursor = connection.cursor()
#     output = None

#     try:
#         cursor.execute(query)
#         output = cursor.fetchall()
#         return output
#     except Error as err:
#         print(f"Error: '{err}'")


# User story 1
def add_coffee_taste_handler(database_name: str):
    # Checks that the user is logged in
    # Asks the user to enter the name of the roastery and coffee
    # the number of points and any notes
    # Then adds those values to the database

    if user_email is None:
        print("You are not logged in, please log in first ")
        return
    coffee_name = input("Enter the name of the coffee you tasted: ")
    roastery_name = input(
        "Enter the name of the roastery where your coffee was roasted: "
    )

    print("Entering points ...")
    _, points = pick(
        [str(i) for i in range(11)],
        "Enter the number of points you would like to give the coffee",
    )
    print("You selected", points, "points")

    notes = input("Write down any notes about the coffee: ")

    add_coffee_taste(
        database_name=database_name,
        email=user_email,
        coffee_name=coffee_name,
        roastery_name=roastery_name,
        points=points,
        notes=notes,
    )


# User story 2
def print_users_with_coffee_tastes(database_name: str):
    # Searches the database for the number of unique coffees each user has tasted
    # Prints the full name of all users who have drunk at least 1 coffee,
    # and the number of coffees they have drunk
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    year = datetime.now().year
    year = f"{year}-01-01"

    print("\nFullName: CoffeesDrunk")
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
def show_coffee_value(database_name: str):
    # Calculates the coffee value as the average rating of the coffee divided by the price
    # Displays the coffee and roastery name, the price, and this value for all coffees that have been rated at least once
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


# generic input sanitizer
def choice_parser(prompt, type_=None, min_=None, max_=None, range_=None):
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ must be less than or equal to max_.")
    while True:
        try:
            ui = type_(ui)
        except ValueError:
            print("Input type must be {0}.".format(type_.__name__))
            continue
        if max_ is not None and ui > max_:
            print("Input must be less than or equal to {0}.".format(max_))
        elif min_ is not None and ui < min_:
            print("Input must be greater than or equal to {0}.".format(min_))
        elif range_ is not None and ui not in range_:
            if isinstance(range_, range):
                template = "Input must be between {0.start} and {0.stop}."
                print(template.format(range_))
            else:
                template = "Input must be {0}."
                if len(range_) == 1:
                    print(template.format(*range_))
                else:
                    expected = " or ".join(
                        (", ".join(str(x) for x in range_[:-1]), str(range_[-1]))
                    )
                    print(template.format(expected))
        else:
            return ui


def main():
    database_name = "test.db"

    # This object describes the different options the user has to search or change the database
    # The "handler" key references one of the functions above
    options = [
        {
            "label": "Log in",
            "confirmation_message": "Logging in\n",
            "handler": log_in,
        },
        {
            "label": "Log out",
            "confirmation_message": "Logging out\n",
            "handler": log_out,
        },
        {
            "label": "Add coffee taste",
            "confirmation_message": "Add a coffee taste selected\n",
            "handler": add_coffee_taste_handler,
        },
        {
            "label": "Print users who have tasted the most coffee",
            "confirmation_message": "Printing the number of coffes each user has drunk\n",
            "handler": print_users_with_coffee_tastes,
        },
        {
            "label": "Print the value and price of each coffee",
            "confirmation_message": "Printing coffee values\n",
            "handler": show_coffee_value,
        },
        # {
        #     "label": "Search coffees based on descriptions",
        #     "confirmation_message": "Coffee description search selected\n",
        #     "handler": search_description,
        # },
        # {
        #     "label": "Search coffees based on farm country and method",
        #     "confirmation_message": "Country and method search selected\n",
        #     "handler": search_country_and_method,
        # },
        {
            "label": "Search after coffees",
            "confirmation_message": "Coffee search selected\n",
            "handler": general_search,
        },
    ]

    title = "What do you want to do?"
    while True:
        print("Selecting options ...")
        selected, _ = pick(
            options, title, options_map_func=lambda option: option.get("label")
        )

        print(selected["confirmation_message"])

        # Run the handler function that was selected
        selected["handler"](database_name)

        feedback = input('\nPress enter to continue or "q" and enter to quit: ').lower()
        if feedback == "q":
            return


if __name__ == "__main__":
    main()
