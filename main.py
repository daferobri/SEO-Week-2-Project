from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text


def main():
    while True:
        reg_or_login = input("Welcome! Register (r) or log in (l): ")
        if reg_or_login == "r" or reg_or_login == "l":
            break
        else:
            print("Invalid input. Please enter (r) to register or (l) to log in.\n")

    engine = create_engine("sqlite:///project.db")
    meta = MetaData()

    users = Table(
        'users', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('phone', String),
        Column('email', String)
    )
    meta.create_all(engine)

    name = input("Name: ")
    phone = input("Phone number: ")
    email = input("Email address: ")

    add = users.insert().values(name=name, phone=phone, email=email)
    
    with engine.connect() as connection:
        connection.execute(add)
        connection.commit()
        

if __name__ == "__main__":
    main()