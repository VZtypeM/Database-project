import pick
import sqlite3


def handle_roastery_description(database_name: str):
    search_term = "%" + input("Enter the term you want to search after: ") + "%"

    return ("Description LIKE ?", search_term)


def handle_user_description(database_name: str):
    search_term = "%" + input("Enter the term you want to search after: ") + "%"

    return ("Notes LIKE ?", search_term)


def handle_processing_method(database_name: str):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute("SELECT MethodName FROM ProcessingMethod;")
    method_names = cursor.fetchall()
    connection.close()

    method_names = [name[0] for name in method_names]

    selected_method, _ = pick.pick(
        method_names, "Which method do you want to search after?"
    )
    return (f'MethodName == "{selected_method}"', None)


def handle_country_search(database_name: str):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute("SELECT DISTINCT Country FROM Location;")
    names = cursor.fetchall()
    connection.close()

    names = [name[0] for name in names]

    if len(names) < 10:
        selection, _ = pick.pick(names, "Which country do you want to search after?")
        return (f'Country == "{selection}"', None)
    else:
        search_prompt = "Enter the name of the country you want to search after: "
        search_term = "%" + input(search_prompt) + "%"

        return ("Country LIKE ?", search_term)


def handle_region_search(database_name: str):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute("SELECT DISTINCT Region FROM Location;")
    names = cursor.fetchall()
    connection.close()

    names = [name[0] for name in names]

    if len(names) < 10:
        selection, _ = pick.pick(names, "Which region do you want to search after?")
        return (f'Region == "{selection}"', None)
    else:
        search_prompt = "Enter the name of the region you want to search after: "
        search_term = "%" + input(search_prompt) + "%"

        return ("Region LIKE ?", search_term)


def general_search(database_name: str):
    input_terms = []
    sql_query = """
    SELECT DISTINCT Roastery.name as RoasteryName, CoffeeName
    FROM Roastery 
    JOIN RoastedCoffee USING (RoasteryID) 
    JOIN CoffeeTastes USING (RoasteryID, CoffeeName) 
    JOIN CoffeeBatch USING (BatchID) 
    JOIN Farm USING (FarmID) 
    JOIN Location USING (LocationID)
    WHERE """

    title_category = "What category do you want to search?"
    options_category = [
        {
            "label": "Coffee description by roastery",
            "handler": handle_roastery_description,
        },
        {
            "label": "Coffee description by users",
            "handler": handle_user_description,
        },
        {
            "label": "Processing method",
            "handler": handle_processing_method,
        },
        {
            "label": "Country",
            "handler": handle_country_search,
        },
        {
            "label": "Region",
            "handler": handle_region_search,
        },
    ]
    title_negate = "Negate last search term?"
    title_new_search = "Do you want to add another search term?"
    options_true_false = ["Yes", "No"]
    title_and_or = "Do you wanna ues AND or OR between your previous search terms and the new one you are about to add?"
    options_and_or = ["AND", "OR"]

    condition_count = 0

    selected_category, _ = pick.pick(
        options_category,
        title_category,
        options_map_func=lambda option: option.get("label"),
    )

    sql_addition, term_addition = selected_category["handler"](database_name)

    selected_negate, _ = pick.pick(options_true_false, title_negate, default_index=1)

    if selected_negate == "Yes":
        sql_query += "NOT "

    sql_query += sql_addition
    if term_addition is not None:
        input_terms.append(term_addition)

    while True:
        selected_another, _ = pick.pick(options_true_false, title_new_search)
        if selected_another == "No":
            break

        selected_and_or, _ = pick.pick(options_and_or, title_and_or)
        sql_query += " " + selected_and_or + " ("

        selected_category, _ = pick.pick(
            options_category,
            title_category,
            options_map_func=lambda option: option.get("label"),
        )
        sql_addition, term_addition = selected_category["handler"](database_name)

        selected_negate, _ = pick.pick(
            options_true_false, title_negate, default_index=1
        )
        if selected_negate == "Yes":
            sql_query += "NOT "

        sql_query += sql_addition
        if term_addition is not None:
            input_terms.append(term_addition)

        condition_count += 1

    sql_query += ")" * condition_count + ";"

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    for row in cursor.execute(sql_query, tuple(input_terms)):
        print(row)
    connection.close()


if __name__ == "__main__":
    general_search("test.db")
