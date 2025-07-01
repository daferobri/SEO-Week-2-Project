from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from geopy.geocoders import Nominatim
import geohash

meta = MetaData()

users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('phone', String),
    Column('loc', String)
)


def get_geohash(user_loc):
    geolocator = Nominatim(user_agent="project")
    location = geolocator.geocode(user_loc)
    
    if not location:
        return None

    geohash_string = geohash.encode(location.latitude, location.longitude)
    return geohash_string


def init_database():
    engine = create_engine("sqlite:///project.db")
    meta.create_all(engine)
    return engine


def add_user(engine, name, phone, loc):
    add = users.insert().values(name=name, phone=phone, loc=loc)
    
    with engine.connect() as connection:
        connection.execute(add)
        connection.commit()


def main():
    engine = init_database()

    while True:
        reg_or_login = input("Welcome! Register (r) or log in (l): ").strip()
        if reg_or_login == "r" or reg_or_login == "l":
            break
        else:
            print("Invalid input. Please enter (r) to register or (l) to log in.\n")

    if reg_or_login == "r":
        while True:
            name = input("Name: ").strip()
            if name:
                break
        
        while True:
            phone = input("Phone number: ").strip()
            if name:
                break
        
        while True:
            loc = input("Location: ").strip()
            if loc:
                loc = get_geohash(loc)
                if loc:
                    break
        
        add_user(engine, name, phone, loc)
    
    else:
        name = input("Name: ").strip()
        with engine.connect() as connection:
            t = users.select().where(users.c.name == name)
            user_info = connection.execute(t).fetchall()
            print(user_info)
    
    # with engine.connect() as connection:
    #     result = connection.execute(text("SELECT * FROM users;")).fetchall()
    #     print(result)
    

if __name__ == "__main__":
    main()