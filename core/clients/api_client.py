import jsonschema
import requests
import os
from dotenv import load_dotenv
from core.settings.environments import Environment
from core.clients.endpoints import Endpoints
from core.settings.config import Users, Timeouts
from tests.schemas.booking_schema import BOOKING_SCHEMA
import allure

load_dotenv()


class APIClient:
    def __init__(self):
        environment_str = os.getenv('ENVIRONMENT')
        try:
            environment = Environment[environment_str]
        except KeyError:
            raise ValueError(f'Unsupported environment value: {environment_str}')

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/json'

        }

    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv('TEST_BASE_URL')
        elif environment == Environment.PROD:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f"Unsupported environment value: {environment}")

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.headers, json=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def ping(self):
        with allure.step("Ping api client"):
            url = f"{self.base_url}{Endpoints.PING_ENDPOINT}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 201, f"Expected status 201 but got {response.status_code}"
            return response.status_code

    def auth(self):
        with allure.step("Getting authentication"):
            url = f"{self.base_url}{Endpoints.AUTH_ENDPOINT}"
            payload = {"username": Users.USERNAME, "password": Users.PASSWORD}
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
        token = response.json().get("token")
        with allure.step("Updating header with authorization"):
            self.session.headers.update({"Authorization:" f"Bearer {token}"})

    def create_booking(self, booking_data):

        with allure.step('Creating booking'):
            url = f"{self.base.url}{Endpoints.BOOKING_ENDPOINT}"
            response = self.session.post(url, json=booking_data)
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
            booking_id = response.json()["bookingid"]
            return booking_id

    def test_add_new_booking(self):
        booking_data = {
            "firstname": "Jim", "lastname": "Brown", "totalprice": 111, "depositpaid": True,
            "additionalneeds": "Breakfast", "bookingdates": {
                "checkin": "2018-01-01", "checkout": "2019-01-01"}
        }

        booking_id = self.create_booking(booking_data)

        with allure.step('Asserting status code and validating JSON'):
            status_code, data = self.get_booking(booking_id)
            assert status_code == 200, f"Expected status 200 but got {status_code}"
            jsonschema.validate(data, BOOKING_SCHEMA)

    def get_booking(self, booking_id):
        with allure.step("Get booking"):
            url = f"{self.base.url}{Endpoints.BOOKING_ENDPOINT}/{booking_id}"
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
        with allure.step('Checking status code and Json Schema'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
            jsonschema.validate(data, BOOKING_SCHEMA)
            return response.status_code, data
