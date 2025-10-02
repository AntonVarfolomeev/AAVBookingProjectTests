import allure
import pytest
import requests

from conftest import generate_random_booking_data, api_client, generate_wrong_booking_data, generate_request_body_without_required_field
from core.clients.api_client import APIClient
from tests.schemas.booking_schema import CREATE_BOOKING_SCHEMA
import jsonschema


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
@allure.story('Test server error')
def test_create_booking_internal_server_error(generate_random_booking_data, mocker, api_client):
    payload = generate_random_booking_data
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(AssertionError, match='Expected status 200 but got 500'):
        api_client.create_booking(payload)


@allure.feature('Test create booking')
@allure.story('Test wrong URL')
def test_create_booking_not_found(generate_random_booking_data, mocker, api_client):
    payload = generate_random_booking_data
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(AssertionError, match='Expected status 200 but got 404'):
        api_client.create_booking(payload)


@allure.feature('Test create booking')
@allure.story('Test wrong HTTP method')
def test_create_booking_wrong_method(generate_random_booking_data, mocker, api_client):
    payload = generate_random_booking_data
    mock_response = mocker.Mock()
    mock_response.status_code = 405
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(AssertionError, match='Expected status 200 but got 405'):
        api_client.create_booking(payload)


@allure.feature('Test create booking')
@allure.story('Test connection with different success code')
def test_create_booking_different_code(generate_random_booking_data, mocker, api_client):
    payload = generate_random_booking_data
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(AssertionError, match='Expected status 200 but got 201'):
        api_client.create_booking(payload)

@allure.feature('Test create booking')
@allure.story('Test connection timeout')
def test_create_booking_timeout(generate_random_booking_data, mocker, api_client):
    payload = generate_random_booking_data
    mocker.patch.object(api_client.session, 'post', side_effect=requests.Timeout)
    with pytest.raises(requests.Timeout):
        api_client.create_booking(payload)

@allure.feature('Test create booking')
@allure.story('Test server unavailability')
def test_create_booking_server_unavailable(generate_random_booking_data, mocker, api_client):
    payload = generate_random_booking_data
    mocker.patch.object(api_client.session, 'post', side_effect=Exception('Server unavailable'))
    with pytest.raises(Exception, match='Server unavailable'):
        api_client.create_booking(payload)

@allure.feature('Test create booking')
@allure.story('Test with wrong header')
def test_create_booking_with_wrong_request_header(generate_random_booking_data, mocker, api_client):
    payload = generate_random_booking_data
    mock_response = mocker.Mock()
    mock_response.status_code = 418
    mock_response.json.return_value = {"error": "I'm a teapot"}
    api_client.session.headers ["Content-Type"] = "text/plain"
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(AssertionError, match='Expected status 200 but got 418'):
        api_client.create_booking(payload)

@allure.feature('Test create booking')
@allure.story('Test with wrong request body')
def test_create_booking_wrong_request_body(generate_wrong_booking_data, mocker, api_client):
    payload = generate_wrong_booking_data
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"error": "Bad request"}
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(AssertionError, match='Expected status 200 but got 400'):
        api_client.create_booking(payload)

@allure.feature('Test create booking')
@allure.story('Test with without required field in request body')
def test_create_booking_missing_required_field(generate_request_body_without_required_field, mocker, api_client):
    payload = generate_request_body_without_required_field
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"error": "Bad request"}
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(AssertionError, match='Expected status 200 but got 400'):
        api_client.create_booking(payload)