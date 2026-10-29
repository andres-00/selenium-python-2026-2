from behave import given, when, then

@given("I am logged in on the inventory page")
def step_impl(context):
    context.driver.get("https://www.saucedemo.com/")
    context.login_page.login("standard_user", "secret_sauce")

@when('I add the product "{product_name}" to the cart')
def step_impl(context, product_name):
    context.inventory_page.add_product_to_cart(product_name)

@then("I should see 1 item in the cart")
def step_impl(context):
    cart_count = context.inventory_page.get_cart_count()
    assert cart_count == "1"
