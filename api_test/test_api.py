from playwright.sync_api import Playwright, APIRequestContext
import pytest
from typing import Generator
from pages_classes import DeleteBookingValid, GetTokenValid, CreateBookingValid, GetTokenInvalid, CreateBookingInvalid
import jsonschema
from itertools import repeat

headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

auth_response_schema = {
    "token": "string"
}

booking_response_schema = {
    "bookingid": {
        "type": "integer"
        },
    "booking": {
        "type": "object",
        "properties": {
            "firstname": {
                "type": "string"
            },
            "lastname": {
                "type": "string"
            },
            "totalprice": {
                "type": "number"
            },
            "depositpaid": {
                "type": "boolean"
            },
            "bookingdates": {
                "type": "object",
                "properties": {
                    "checkin": {
                        "type": "string"
                    },
                    "checkout": {
                        "type": "string"
                    }
                }
            },
            "additionalneeds": {
                "type": "string"
            },
            "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"]
        }
    },
    "required": ["bookingid", "booking"]
}

valid_token_test = GetTokenValid()
invalid_token_test = GetTokenInvalid()
valid_booking_test = CreateBookingValid()
invalid_booking_test = CreateBookingInvalid()


@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(
        base_url="https://restful-booker.herokuapp.com"
    )
    yield request_context
    request_context.dispose()


@pytest.mark.parametrize("data,auth_token_url", zip(valid_token_test.make_data(), repeat(valid_token_test.make_request())))
def test_auth_token_valid(api_request_context: APIRequestContext, data, auth_token_url):
    global headers
    
    resp = api_request_context.post(
        auth_token_url, 
        data = data
        )
    
    assert resp.ok
    
    jsonschema.validate(resp.json(), auth_response_schema)
    
    headers |= {"Cookie": f"token={resp.json()["token"]}"}


@pytest.mark.parametrize("data,auth_token_url", zip(invalid_token_test.make_data(), repeat(invalid_token_test.make_request())))
def test_auth_token_invalid(api_request_context: APIRequestContext, data, auth_token_url):
    resp = api_request_context.post(
        auth_token_url, 
        data = data
        )

    assert resp.ok

@pytest.mark.parametrize("data,booking_url", zip(valid_booking_test.make_data(), repeat(valid_booking_test.make_request())))
def test_booking_create_valid(api_request_context: APIRequestContext, data, booking_url):    
    resp = api_request_context.post(
        booking_url, 
        data = data
        )
    
    assert resp.ok

    jsonschema.validate(resp.json(), booking_response_schema)
    
    deletion = api_request_context.delete(DeleteBookingValid(resp.json()["bookingid"]).make_request(), headers = headers)

    assert deletion.ok

@pytest.mark.parametrize("data,booking_url", zip(invalid_booking_test.make_data(), repeat(invalid_booking_test.make_request())))
def test_booking_create_invalid(api_request_context: APIRequestContext, data, booking_url):
    resp = api_request_context.post(
        booking_url, 
        data = data
        )
    
    assert not resp.ok
