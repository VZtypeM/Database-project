from pick import pick
import sqlite3
from tabulate import tabulate

# These handle functions are called when the user wants to search a spesific category
# They all return a part of an SQL query and maybe the input the user entered that must
# must be sanitized
def handle_roastery_description(database_name: str) -> tuple:
    search_term = "%" + input("Enter the term you want to search after: ") + "%"

    return ("Description LIKE ?", search_term)


def handle_user_description(database_name: str) -> tuple:
    search_term = "%" + input("Enter the term you want to search after: ") + "%"

    return ("Notes LIKE ?", search_term)


def handle_processing_method(database_name: str) -> tuple:
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute("SELECT MethodName FROM ProcessingMethod;")
    method_names = cursor.fetchall()
    connection.close()

    method_names = [name[0] for name in method_names]

    print("Selecting method name ...")
    selected_method, _ = pick(method_names, "Which method do you want to search after?")
    return (f'MethodName == "{selected_method}"', None)


def handle_farm_country_search(database_name: str) -> tuple:
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute("SELECT Country FROM Country;")
    names = cursor.fetchall()
    connection.close()

    names = [name[0] for name in names]

    # Askes the user to select among countries if there are fewer than 10 countries
    # Otherwise asks the user to enter the name of the country manually
    if len(names) < 10:
        print("Selecting country ...")
        selection, _ = pick(names, "Which country do you want to search after?")
        return (f'Farm.Country == "{selection}"', None)
    else:
        search_prompt = "Enter the name of the country you want to search after: "
        search_term = "%" + input(search_prompt) + "%"

        return ("Farm.Country LIKE ?", search_term)


def handle_farm_region_search(database_name: str) -> tuple:
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute("SELECT Region FROM Region;")
    names = cursor.fetchall()
    connection.close()

    names = [name[0] for name in names]

    # Askes the user to select among regions if there are fewer than 10 regions
    # Otherwise asks the user to enter the name of the region manually
    if len(names) < 10:
        print("Selecting region ...")
        selection, _ = pick(names, "Which region do you want to search after?")
        return (f'Farm.Region == "{selection}"', None)
    else:
        search_prompt = "Enter the name of the region you want to search after: "
        search_term = "%" + input(search_prompt) + "%"

        return ("Farm.Region LIKE ?", search_term)


# User story 4 and 5
def general_search(database_name: str):
    # Note that the query also includes the roasteryID. This id is not displayed,
    # but including it here makes sure that coffees from roasteries with identical names are still shown
    # Since we allow coffees to have the same roatery and coffee name, it would also be beneficial to show the
    # location or the id of the roastery to fully identify it, but this is not specified by the user stories.
    input_terms = []
    sql_query = """
    SELECT DISTINCT Roastery.name as RoasteryName, CoffeeName, RoasteryID
    FROM Roastery 
    JOIN RoastedCoffee USING (RoasteryID) 
    LEFT OUTER JOIN CoffeeTastes USING (RoasteryID, CoffeeName) 
    JOIN CoffeeBatch USING (BatchID) 
    JOIN Farm USING (FarmID) 
    WHERE """
    # As you can see all relevant tables are allready joined,
    # so this program could be further optimized by only joining
    # with the tables needed by the search specified by the user

    # Titles and options used by the pick library:
    title_category = "What category do you want to search?"
    options_category = [
        {
            "label": "Coffee description by roastery",
            "confirmation_message": "Coffee description by roastery category chosen",
            "handler": handle_roastery_description,
        },
        {
            "label": "Coffee description by users",
            "confirmation_message": "Coffee description by users category chosen",
            "handler": handle_user_description,
        },
        {
            "label": "Processing method",
            "confirmation_message": "Processing method category chosen",
            "handler": handle_processing_method,
        },
        {
            "label": "Farm country",
            "confirmation_message": "Farm country category chosen",
            "handler": handle_farm_country_search,
        },
        {
            "label": "Farm region",
            "confirmation_message": "Farm region category chosen",
            "handler": handle_farm_region_search,
        },
    ]
    title_negate = "Negate last search term?"
    title_new_search = "Do you want to add another search term?"
    options_true_false = ["Yes", "No"]
    title_and_or = "Do you wanna ues AND or OR between your previous search terms and the new one you are about to add?"
    options_and_or = ["AND", "OR"]

    # The number of conditions you entered
    # Used for adding the correct number of parentheses at the end
    condition_count = 0

    while True:
        # Select category
        print("Selecting search category ...")
        selected_category, _ = pick(
            options_category,
            title_category,
            options_map_func=lambda option: option.get("label"),
        )
        print(selected_category["confirmation_message"])

        # Call the handler function in the options_category object
        sql_addition, term_addition = selected_category["handler"](database_name)

        # Ask if the user want to negate its search, and adds "NOT" to the sql_query if they do
        print("Selecting whether to negate the search term ...")
        selected_negate, _ = pick(options_true_false, title_negate, default_index=1)
        if selected_negate == "Yes":
            sql_query += "NOT "

        # Append the query returned by the handler function after "NOT" has had a chance to be added
        sql_query += sql_addition
        if term_addition is not None:
            input_terms.append(term_addition)

        # Asks if the user wants to select another search term
        print("Selecting whether to add another search term ...")
        selected_another, _ = pick(options_true_false, title_new_search)
        if selected_another == "No":
            break
        condition_count += 1

        # Asks how the user want to append the new query ("AND" or "OR")
        print("Selecting AND or OR ...")
        selected_and_or, _ = pick(options_and_or, title_and_or)
        sql_query += " " + selected_and_or + " ("

    sql_query += ")" * condition_count + ";"

    # Printing the query so the user can double check that what is shown is what they asked for
    print("Executing the following query: ")
    print(sql_query)
    if len(input_terms) > 0:
        print("\nWith the follwing input")
        print(input_terms)

    # Fetching the data
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute(sql_query, tuple(input_terms))
    result = cursor.fetchall()
    connection.close()

    # Remove the roastery ID at the end of the data
    for i in range(len(result)):
        result[i] = result[i][:2]

    # Printing the result
    if len(result) == 0:
        print("\nThis query returned 0 coffees")
        return

    print("\nThe result of this query was: ")
    print(tabulate(result, headers=["Roastery name", "Coffee name"], tablefmt="github"))


# If this python file is run (and not imported) run the general_search function
if __name__ == "__main__":
    general_search("src/coffee.db")
