import json

valid_jsons = json.load(open("valid_data.json", "r"))
invalid_jsons = json.load(open("invalid_data.json", "r"))

class BaseTestUrl:
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def make_request(self) -> str:
        return self.url
    
    def make_data(self) -> list[dict[str, str | int | bool | dict | list]]:
        return self.data


class GetTokenValid(BaseTestUrl):
    def __init__(self) -> None:
        self.url = "/auth"
        self.data = valid_jsons["username_password"]


class GetTokenInvalid(GetTokenValid):
    def __init__(self) -> None:
        super().__init__()
        self.data = invalid_jsons["username_password"]


class CreateBookingValid(BaseTestUrl):
    def __init__(self) -> None:
        self.url = "/booking"
        self.data = valid_jsons["booking"]


class CreateBookingInvalid(CreateBookingValid):
    def __init__(self) -> None:
        super().__init__()
        self.data = invalid_jsons["booking"]


class DeleteBookingValid(BaseTestUrl):
    def __init__(self, booking_id: str | int) -> None:
        self.url = "/booking/" + str(booking_id) 
