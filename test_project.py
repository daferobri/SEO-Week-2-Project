import unittest
from ticket_events import format_date_for_tmAPI
from database import add_user, get_user_by_name, init_database

def test_data_format_for_tm():
    start_utc, end_utc = format_date_for_tmAPI("2025-07-10") #Expects YYYY-MM-DD

    assert isinstance(start_utc, str)
    assert isinstance(end_utc, str)

    #check that start and end time are different
    assert start_utc != end_utc


def test_add_user_succesfully():
    engine = init_database()
    result = add_user(engine, "test_user", "testemail@email.com", "Phoenix, AZ")
    user = get_user_by_name(engine, "test_user")
    assert user is not None
    assert user['name'] == "test_user"


def test_get_user_by_name():
    engine = init_database()
    
    add_user(engine, "Admin", "random@email.com", "Phoenix, AZ")

    user = get_user_by_name(engine, "Admin")
    user1 = get_user_by_name(engine, "fakeName")
    assert user is not None
    assert user1 is not None


if __name__ == "__main__":
    test_data_format_for_tm()
    test_add_user_succesfully()
    test_get_user_by_name()


