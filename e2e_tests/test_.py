from playwright.sync_api import Page, expect
from pageobjs.login_po import LoginPage
from pageobjs.cart_po import CartPage
from pageobjs.items_po import ShopPage

def test_login_w_wrong_login_pw(page: Page):
    loginpg = LoginPage(page)

    loginpg.navigate()

    loginpg.login("wrong_user", "bad_password")

    expect(loginpg.check_error()).to_contain_text("Epic sadface: Username and password do not match any user in this service")

    
def test_login_wo_username(page: Page):
    loginpg = LoginPage(page)

    loginpg.navigate()

    loginpg.login()

    expect(loginpg.check_error()).to_contain_text("Epic sadface: Username is required")

def test_adding_one_item_to_cart(page: Page):
    loginpg = LoginPage(page)
    shoppg = ShopPage(page)
    cartpg = CartPage(page)

    loginpg.navigate()
    loginpg.login("standard_user", "secret_sauce")

    shoppg.navigate()
    shoppg.buy_backpack()

    cartpg.navigate()

    expect(shoppg.check_shopping_cart_badge()).to_have_text("1")
    expect(cartpg.check_backpack_item_label()).to_be_visible()
