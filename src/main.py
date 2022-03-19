import pick
import sqlite3
from add_coffee_taste import add_coffee_taste
from datetime import datetime
from general_search import general_search

user_email = None


def log_in(database_name: str):
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
    if user_email is None:
        print("You are not logged in, please log in first: ")
        return
    coffee_name = input("Enter the name of the coffee you tasted: ")
    roastery_name = input(
        "Enter the name of the roastery where your coffee was roasted: "
    )

    # Error handling
    msg = "Enter the number of points you would like to give the coffee, between 0-10:"
    valid = False
    while not valid:
        points = input(msg)
        try:
            points = int(points)
        except ValueError:
            msg = "Please enter integer values."
        else:
            valid = points >= 0 and points <= 10
            if not valid:
                msg = "Enter an integer between 0 and 10."
            print(f"You have entered {points}.")

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
def search_description(database_name: str):
    search_term = "%" + input("Enter the term you want to search after: ") + "%"

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


# User story 5
def search_country_and_method(database_name: str):
    # TODO: Should instead have a more general search
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
        JOIN Location USING (LocationID)
        WHERE MethodName LIKE ? OR Country LIKE ?;
        """,
        (search_method, search_country),
    ):
        print(f"{row[0]}, {row[1]}")

    connection.close()


# Generic input sanitizer
# def choice_parser(prompt, type_=None, min_=None, max_=None, range_=None):
#     if min_ is not None and max_ is not None and max_ < min_:
#         raise ValueError("min_ must be less than or equal to max_.")
#     while True:
#         ui = input(prompt)
#         if type_ is not None:
#             try:
#                 ui = type_(ui)
#             except ValueError:
#                 print("Input type must be {0}.".format(type_.__name__))
#                 continue
#         if max_ is not None and ui > max_:
#             print("Input must be less than or equal to {0}.".format(max_))
#         elif min_ is not None and ui < min_:
#             print("Input must be greater than or equal to {0}.".format(min_))
#         elif range_ is not None and ui not in range_:
#             if isinstance(range_, range):
#                 template = "Input must be between {0.start} and {0.stop}."
#                 print(template.format(range_))
#             else:
#                 template = "Input must be {0}."
#                 if len(range_) == 1:
#                     print(template.format(*range_))
#                 else:
#                     expected = " or ".join(
#                         (", ".join(str(x) for x in range_[:-1]), str(range_[-1]))
#                     )
#                     print(template.format(expected))
#         else:
#             return ui


def main():
    database_name = "test.db"

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
        {
            "label": "Search farm country and method",
            "confirmation_message": "Searching",
            "handler": search_country_and_method,
        },
        {
            "label": "Search the database for coffees",
            "confirmation_message": "",
            "handler": general_search,
        },
    ]

    title = "What do you want to do?"
    while True:
        selected = pick.pick(
            options, title, options_map_func=lambda option: option.get("label")
        )

        print(selected[0]["confirmation_message"])

        # Run the handler function you selected
        selected[0]["handler"](database_name)

        feedback = input('Press enter to continue or "q" to quit: ').lower()
        if feedback == "q":
            return


if __name__ == "__main__":
    main()
