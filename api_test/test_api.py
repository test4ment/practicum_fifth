from playwright.sync_api import Playwright, APIRequestContext
import pytest
from typing import Generator
from pages_classes import GetTokenUrl, CreateBookingUrl, sample_booking

headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
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
    assert resp.json()["token"]
    
    headers |= {"Authorization": f"Basic {resp.json()["token"]}"}


def test_booking_create(api_request_context: APIRequestContext):
    booking_create_url_data = CreateBookingUrl()
    
    resp = api_request_context.post(
        booking_create_url_data.make_request(), 
        data = booking_create_url_data.make_data()
        )
    
    assert resp.ok

    assert all([key in resp.json() for key in {"booking", "bookingid"}])
    assert all([key in resp.json()["booking"] for key in sample_booking.keys()])
