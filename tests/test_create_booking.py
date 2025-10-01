import allure
import pytest
import requests

from conftest import generate_random_booking_data
from core.clients.api_client import APIClient
from tests.schemas.booking_schema import CREATE_BOOKING_SCHEMA
import jsonschema


@allure.feature('Test create booking')
@allure.story('Test positive script with valid info')
def test_create_booking_success(generate_random_booking_data, api_client):
    with allure.step("Preparing data for creating booking"):
        payload = generate_random_booking_data
        client = api_client
        response = client.create_booking(payload)

    with allure.step("Validating JSON schema"):
        jsonschema.validate(response, CREATE_BOOKING_SCHEMA)

    with allure.step("Validating response data"):
        assert 'bookingid' in response, "Booking ID isn't equal to expected"
        assert payload['firstname'] == response['booking']['firstname'], "Booking firstname isn't equal to expected"
        assert payload['lastname'] == response['booking']['lastname'], "Booking lastname isn't equal to expected"
        assert payload['totalprice'] == response['booking']['totalprice'], "Booking totalprice isn't equal to expected"
        assert payload['depositpaid'] == response['booking']['depositpaid'], "Booking depositpaid isn't equal to expected"
        assert payload['bookingdates']['checkin'] == response['booking']['bookingdates'][
            'checkin'], "Booking checkin isn't equal to expected"
        assert payload['bookingdates']['checkout'] == response['booking']['bookingdates'][
            'checkout'], "Booking checkout isn't equal to expected"
        assert payload['additionalneeds'] == response['booking']['additionalneeds'], "Booking additionalneeds isn't equal to expected"




