from playwright.sync_api import Page

class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.backpack_item_label = page.locator("[data-test=\"item-4-title-link\"]")
        
    def navigate(self):
        self.page.goto("https://www.saucedemo.com/cart.html")

    def check_backpack_item_label(self):
        return self.backpack_item_label

