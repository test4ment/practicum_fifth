from playwright.sync_api import Playwright, APIRequestContext
import pytest
from typing import Generator
from pages_classes import DeleteBookingUrl, GetTokenUrl, CreateBookingUrl, sample_booking
import jsonschema

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


@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(
        base_url="https://restful-booker.herokuapp.com"
    )
    yield request_context
    request_context.dispose()

@pytest.fixture(scope="session", autouse=True)
def get_auth_token(api_request_context: APIRequestContext):
    test_auth_token(api_request_context)


def test_auth_token(api_request_context: APIRequestContext):
    global headers
    
    auth_token_url = GetTokenUrl()
    resp = api_request_context.post(
        auth_token_url.make_request(), 
        data = auth_token_url.make_data()
        )
    
    assert resp.ok
    
    jsonschema.validate(resp.json(), auth_response_schema)
    
    headers |= {"Cookie": f"token={resp.json()["token"]}"}


def test_booking_create(api_request_context: APIRequestContext):
    booking_create_url_data = CreateBookingUrl()
    
    resp = api_request_context.post(
        booking_create_url_data.make_request(), 
        data = booking_create_url_data.make_data()
        )
    
    assert resp.ok

    jsonschema.validate(resp.json(), booking_response_schema)
    
    deletion = api_request_context.delete(DeleteBookingUrl(resp.json()["bookingid"]).make_request(), headers = headers)

    assert deletion.ok
