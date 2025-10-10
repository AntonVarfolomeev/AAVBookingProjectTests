import os
import allure
import pytest
import requests

from conftest import generate_random_booking_data, api_client, generate_wrong_booking_data, \
    generate_request_body_without_mandatory_field, generate_empty_request_body
from core.clients.api_client import APIClient
from tests.schemas.booking_schema import CREATE_BOOKING_SCHEMA
import jsonschema
from dotenv import load_dotenv

load_dotenv()


@allure.feature('Test create booking')
@allure.story('Test positive script with valid info')
def test_create_booking_success(generate_random_booking_data, api_client):
    with allure.step("Preparing data for creating booking"):
        payload = generate_random_booking_data
        response = api_client.create_booking(payload)

    with allure.step("Validating JSON schema"):
        jsonschema.validate(response, CREATE_BOOKING_SCHEMA)

    with allure.step("Validating response data"):
        assert 'bookingid' in response, "Booking ID isn't equal to expected"
        assert payload['firstname'] == response['booking']['firstname'], "Booking firstname isn't equal to expected"
        assert payload['lastname'] == response['booking']['lastname'], "Booking lastname isn't equal to expected"
        assert payload['totalprice'] == response['booking']['totalprice'], "Booking totalprice isn't equal to expected"
        assert payload['depositpaid'] == response['booking'][
            'depositpaid'], "Booking depositpaid isn't equal to expected"
        assert payload['bookingdates']['checkin'] == response['booking']['bookingdates'][
            'checkin'], "Booking checkin isn't equal to expected"
        assert payload['bookingdates']['checkout'] == response['booking']['bookingdates'][
            'checkout'], "Booking checkout isn't equal to expected"
        assert payload['additionalneeds'] == response['booking'][
            'additionalneeds'], "Booking additionalneeds isn't equal to expected"


@allure.feature('Test create booking')
@allure.story('Test where mandatory field "depositpaid" has invalid data type')
def test_create_booking_wrong_request_body(generate_wrong_booking_data, api_client):
    payload = generate_wrong_booking_data
    api_client.create_booking(payload)


@allure.feature('Test create booking')
@allure.story('Test with missed mandatory field in request body')
def test_create_booking_missing_mandatory_field(generate_request_body_without_mandatory_field, api_client):
    payload = generate_request_body_without_mandatory_field
    with pytest.raises(AssertionError, match='Expected status 200 but got 500'):
        api_client.create_booking(payload)


@allure.feature('Test create booking')
@allure.story('Test with empty JSON in request')
def test_create_booking_with_empty_json(generate_empty_request_body, api_client):
    payload = generate_empty_request_body
    with pytest.raises(AssertionError, match='Expected status 200 but got 500'):
        api_client.create_booking(payload)