from multipledispatch import dispatch
from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("[data-test=\"username\"]")
        self.password = page.locator("[data-test=\"password\"]")
        self.login_button = page.locator("[data-test=\"login-button\"]")
        self.error = page.locator("[data-test=\"error\"]")

    def navigate(self):
        self.page.goto("https://www.saucedemo.com/")

    @dispatch(str, str)
    def login(self, username: str, password: str):
        self.username.click()
        self.username.fill(username)
        self.password.click()
        self.password.fill(password)
        self.login()
    
    @dispatch()
    def login(self):
        self.login_button.click()
    
    def check_error(self):
        return self.error
