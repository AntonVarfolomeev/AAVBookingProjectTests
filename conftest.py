from core.clients.api_client import APIClient
from datetime import datetime, timedelta
from faker import Faker
import pytest
import requests
from core.clients.endpoints import Endpoints


@pytest.fixture(scope="session")
def api_client():
    client = APIClient()
    client.auth()
    return client


@pytest.fixture()
def booking_dates():
    today = datetime.today()
    checkin_date = today + timedelta(days=10)
    checkout_date = checkin_date + timedelta(days=5)

    return {
        "checkin": checkin_date.strftime('%Y-%m-%d'),
        "checkout": checkout_date.strftime('%Y-%m-%d')
    }


@pytest.fixture()
def generate_random_booking_data(booking_dates):
    faker = Faker()
    firstname = faker.first_name()
    lastname = faker.last_name()
    totalprice = faker.random_number(digits=3)
    depositpaid = faker.boolean()
    additionalneeds = faker.sentence()

    data = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": booking_dates,
        "additionalneeds": additionalneeds
    }

    return data

@pytest.fixture()
def generate_wrong_booking_data(booking_dates):
    faker = Faker()
    firstname = faker.first_name()
    lastname = faker.last_name()
    totalprice = faker.boolean()
    depositpaid = "not_boolean"
    additionalneeds = faker.sentence()

    data = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": booking_dates,
        "additionalneeds": additionalneeds
    }

    return data


@pytest.fixture()
def generate_request_body_without_mandatory_field(booking_dates):
    faker = Faker()
    firstname = faker.first_name()
    totalprice = faker.random_number(digits=3)
    depositpaid = faker.boolean()
    additionalneeds = faker.sentence()

    data = {
        "firstname": firstname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": booking_dates,
        "additionalneeds": additionalneeds
    }

    return data

@pytest.fixture()
def generate_empty_request_body():

    data = {}

    return data