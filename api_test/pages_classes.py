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

class DeleteBookingUrl(BaseTestUrl):
    def __init__(self, booking_id: str | int) -> None:
        self.url = str(booking_id) 
