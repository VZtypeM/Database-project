import pick
import add_coffee_taste


def log_in(database_name: str):
    print("logging in")


def log_out(database_name: str):
    pass


def add_coffee_taste_handler(database_name: str):
    add_coffee_taste.add_coffee_taste(
        database_name=database_name,
        email="ola.nordman@gmail.com",
        coffee_name="Vinterkaffe 2022",
        roastery_name="Trondheim brewery Jacobsen & Svart",
        points=4,
        notes="Splendid",
    )


def main():
    database_name = "test.db"
    options = [
        {"label": "log in", "handler": log_in},
        {"label": "log out", "handler": log_out},
        {"label": "add coffee taste", "handler": add_coffee_taste_handler},
    ]

    title = "What do you want to do?"
    selected = pick.pick(
        options, title, options_map_func=lambda option: option.get("label")
    )

    # Run the handler function you selected
    selected[0]["handler"](database_name)

    # if selected[0] == "add coffee taste":
    #     add_coffee_taste(
    #         "ola.nordman@gmail.com",
    #         "Vinterkaffe 2022",
    #         "Trondheim brewery Jacobsen & Svart",
    #         7,
    #         "Splendid",
    #     )


if __name__ == "__main__":
    main()
