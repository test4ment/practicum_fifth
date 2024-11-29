from playwright.sync_api import Playwright, APIRequestContext
import pytest
from typing import Generator

headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

sample_booking = {
                    "firstname" : "Michael",
                    "lastname" : "White",
                    "totalprice" : 1337,
                    "depositpaid" : False,
                    "bookingdates" : {
                        "checkin" : "9999-31-12",
                        "checkout" : "10000-99-99"
                    },
                    "additionalneeds" : "Playwright autotest"
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
    

class BaseTestUrl:
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def make_request(self) -> str:
        return self.url
    
    def make_data(self) -> dict[str, str | int | bool | dict | list]:
        return self.data
    
class GetTokenUrl(BaseTestUrl):
    def __init__(self) -> None:
        self.url = "/auth"
        self.data = {
            "username": "admin",
            "password": "password123"
        }

class CreateBookingUrl(BaseTestUrl):
    def __init__(self) -> None:
        self.url = "/booking"
        self.data = sample_booking