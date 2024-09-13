from playwright.sync_api import Page

class ShopPage:
    def __init__(self, page: Page):
        self.page = page

        self.backpack_add_to_cart_button = page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]")
        self.menu = page.get_by_role("button", name="Open Menu")
        self.shopping_cart_badge = page.locator("[data-test=\"shopping-cart-badge\"]") 
        self.menu_resetapp = page.locator("[data-test=\"reset-sidebar-link\"]")
        self.menu_logout = page.locator("[data-test=\"logout-sidebar-link\"]")

    def navigate(self):
        self.page.goto("https://www.saucedemo.com/inventory.html")
    
    def buy_backpack(self):
        self.backpack_add_to_cart_button.click()
    
    def reset_app_state(self):
        self.menu.click()
        self.menu_resetapp.click()
        self.menu_logout.click()

    def check_shopping_cart_badge(self):
        return self.shopping_cart_badge
