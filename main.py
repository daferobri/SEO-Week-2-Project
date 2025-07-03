from ticket_events import fetch_events_for_user, show_saved_events, fetch_events_and_send_email
from database import init_database, get_user_by_name, add_user, get_coordinates


def main():
    engine = init_database()

    while True:
        reg_or_login = input("Welcome! Register (r) or log in (l): ").strip()
        if reg_or_login == "r" or reg_or_login == "l":
            break
        else:
            print("Invalid input. Enter (r) to register or (l) to log in.\n")

    if reg_or_login == "r":
        name = input("Name: ").strip()
        email = input("Email: ").strip()
        loc = get_coordinates(input("Location: ").strip())
        add_user(engine, name, email, loc)
        username = name
        user_email = email
    else:
        username = input("Name: ").strip()
        user = get_user_by_name(engine, username)

        if not user:
            print("User does not exist, Please Register an account first or check your username")
            return
        user_email = user['email']

    while True:
        action = input("Press 's' to Search events, 'v' to view saved events, 'e' to email events,  or any other letter to quit: ")
        if action == 's':
            date_for_events = input("Enter the date for events in this format (YYYY-MM-DD): ")
            fetch_events_for_user(engine, username, date_for_events)
        elif action == 'v':
            show_saved_events(engine, username)
        elif action == 'e':
            date_for_events = input("Enter the date for events in this format (YYYY-MM-DD): ")
            fetch_events_and_send_email(engine, username, date_for_events, True, user_email)
        else:
            print("Exiting Out the Program")
            break


if __name__ == "__main__":
    main()
