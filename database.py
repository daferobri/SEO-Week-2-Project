from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    text,
)
from geopy.geocoders import Nominatim

meta = MetaData()

users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String),
    Column('loc', String),
    Column('saved_events', String)
)


def save_event_for_user(engine, user_id, tm_event_id):
    user = get_user_by_id(engine, user_id)
    if user['saved_events']:
        saved_events_list = user['saved_events'].split(',')
    else:
        saved_events_list = []
    # check if the event was already saved
    if tm_event_id in saved_events_list:
        return False

    saved_events_list.append(tm_event_id)
    saved_events_as_string = ','.join(saved_events_list)

    with engine.connect() as connection:
        query = users.update().where(
            users.c.id == user_id).values(
            saved_events=saved_events_as_string)
        connection.execute(query)
        connection.commit()
        return True


def get_saved_events(engine, user_id):
    user = get_user_by_id(engine, user_id)
    if not user or not user['saved_events']:
        return []
    return user['saved_events'].split(',')


def get_coordinates(user_loc):
    geolocator = Nominatim(user_agent="project")
    location = geolocator.geocode(user_loc)
    coords = f"{location.latitude},{location.longitude}"
    if location:
        return coords
    else:
        print("Invalid location, please try again.")
        return None


def init_database():
    engine = create_engine("sqlite:///project.db")
    meta.create_all(engine)
    return engine


def add_user(engine, name, email, loc):
    add = users.insert().values(
        name=name,
        email=email,
        loc=loc,
        saved_events=''
    )
    with engine.connect() as connection:
        connection.execute(add)
        connection.commit()


def get_user_by_name(engine, name):
    with engine.connect() as connection:
        query = users.select().where(
            users.c.name == name)
        result = connection.execute(
            query).fetchone()
        if result:
            return {
                'id': result[0],
                'name': result[1],
                'email': result[2],
                'loc': result[3],
                'saved_events': result[4]
            }
        else:
            return None


def get_user_by_id(engine, user_id):
    with engine.connect() as connection:
        query = users.select().where(
            users.c.id == user_id)
        result = connection.execute(
            query).fetchone()
        if result:
            return {
                'id': result[0],
                'name': result[1],
                'email': result[2],
                'loc': result[3],
                'saved_events': result[4]
            }
        return None


def update_user(engine, user_id, name=None, email=None,
                loc=None):
    update_info = {}
    if name:
        update_info['name'] = name
    if email:
        update_info['email'] = email
    if loc:
        update_info['loc'] = loc

    if update_info:
        with engine.connect() as connection:
            if name:
                connection.execute(
                    users.update().where(
                        users.c.id == user_id
                    ).values(name=name)
                )
            if email:
                connection.execute(
                    users.update().where(
                        users.c.id == user_id
                    ).values(email=email)
                )
            if loc:
                connection.execute(
                    users.update().where(
                        users.c.id == user_id
                    ).values(loc=loc)
                )
            connection.commit()
