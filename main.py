import sqlalchemy as db

while True:
    reg_or_login = input("Welcome! Register (r) or log in (l): ")
    if reg_or_login == 'r' or reg_or_login == 'l':
        break
    else:
        print("Invalid input. Please enter 'r' to register or 'l' to log in.\n")
