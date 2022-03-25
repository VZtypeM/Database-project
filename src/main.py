from pick import pick
from tabulate import tabulate
import sqlite3
import add_coffee_taste
from datetime import datetime
from general_search import general_search

# We know, we know, global variables are bad practice, but it makes the code easier and more readable
user_email = None


def log_in(database_name: str) -> None:
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

    print("Logged in")
    # Set the email of the new user
    user_email = result[0][0]


def log_out(database_name: str) -> None:
    # Sets the global user_emal variable to None
    global user_email
    user_email = None


# User story 1
def add_coffee_taste_handler(database_name: str) -> None:
    # Checks that the user is logged in
    # Asks the user to enter the name of the roastery and coffee
    # Asks the user to specify the location of the roastery if the roastery
    # is ambigous only knowing the roastery and coffee name
    # Asks the user to enter the number of points and any notes
    # Then adds those values to the database
    if user_email is None:
        print("You are not logged in, please log in first ")
        return
    coffee_name = input("Enter the name of the coffee you tasted: ")
    roastery_name = input(
        "Enter the name of the roastery where your coffee was roasted: "
    )

    roastery_id = add_coffee_taste.find_roastery_id_from_names(
        database_name, coffee_name, roastery_name
    )
    if roastery_id is None:
        print("Database not modified")
        return

    print("Entering points ...")
    _, points = pick(
        [str(i) for i in range(11)],
        "Enter the number of points you would like to give the coffee",
    )
    print("You selected", points, "points")

    notes = input("Write down any notes about the coffee: ")

    add_coffee_taste.add_coffee_taste(
        database_name=database_name,
        email=user_email,
        coffee_name=coffee_name,
        roastery_id=roastery_id,
        points=points,
        notes=notes,
    )


# User story 2
def print_users_with_coffee_tastes(database_name: str) -> None:
    # Searches the database for the number of unique coffees each user has tasted
    # Prints the full name of all users who have drunk at least 1 coffee,
    # and the number of coffees they have drunk
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    year = datetime.now().year
    year = f"{year}-01-01"

    cursor.execute(
        # The COUNT(DISTINCT RoasteryID || CoffeeName) counts the number of rows having
        # RoasteryID concatinated with CoffeeName unique.
        """
        SELECT FullName, COUNT(DISTINCT RoasteryID || CoffeeName) as CoffeesDrunk
        FROM CoffeeTastes JOIN Roastery USING (RoasteryID) JOIN User USING (email)
        WHERE date >= ?
        GROUP BY email
        ORDER BY CoffeesDrunk DESC;
        """,
        (year,),
    )

    print(
        tabulate(
            cursor.fetchall(),
            headers=["User full name", "Different coffees drunk"],
            tablefmt="github",
        )
    )

    connection.close()


# User story 3
def show_coffee_value(database_name: str) -> None:
    # Calculates the coffee value as the average rating of the coffee divided by the price
    # Displays the coffee and roastery name, the price, and this value for all coffees that have been rated at least once
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute(
        # Note that we are sorting on something different than what is shown
        """
        SELECT Roastery.name as RoasteryName, CoffeeName, PricePerKilo, AVG(Points) as AverageScore
        FROM Roastery JOIN RoastedCoffee USING (RoasteryID) JOIN CoffeeTastes USING (RoasteryID, CoffeeName)
        GROUP BY RoasteryID, CoffeeName
        ORDER BY AVG(Points)/PricePerKilo DESC;
        """
    )
    result = cursor.fetchall()

    cursor.execute(
        # This query only gets the coffees without a rating, which are listet at the bottom
        """
        SELECT Roastery.name as RoasteryName, CoffeeName, PricePerKilo
        FROM Roastery JOIN RoastedCoffee USING (RoasteryID) LEFT OUTER JOIN CoffeeTastes USING (RoasteryID, CoffeeName)
        WHERE email IS NULL;
        """
    )
    no_rating_coffees = cursor.fetchall()
    connection.close()

    for i in range(len(no_rating_coffees)):
        no_rating_coffees[i] = list(no_rating_coffees[i])
        no_rating_coffees[i].append("No rating")

    result.extend(no_rating_coffees)

    print(
        tabulate(
            result,
            headers=[
                "Roastery name",
                "Coffee name",
                "Price per kilo",
                "Average user rating",
            ],
            tablefmt="github",
            colalign=("left", "left", "right", "right"),
        )
    )


def reset_database(database_name: str) -> None:
    with open("src/coffee.sql", "r") as sql_file:
        sql_script = sql_file.read()

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.executescript(sql_script)
    connection.commit()
    connection.close()


def main() -> None:
    database_name = "src/coffee.db"

    # Uncomment the following line to reset the database by running the coffee.sql file
    # reset_database(database_name)

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
            "confirmation_message": "Printing the number of different coffes each user has drunk so far this year\n",
            "handler": print_users_with_coffee_tastes,
        },
        {
            "label": "Print the value and price of each coffee",
            "confirmation_message": "Printing coffee values sorted on average_rating/price\n",
            "handler": show_coffee_value,
        },
        # These commented out options correspond to the spesific queries to solve user story 4 and 5
        # User story 4 and 5 are now solved by the general_search
        # Our previous way of doing it can be found in "not_used.py"
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


# If this python file is run (and not imported) run the main function
if __name__ == "__main__":
    main()
