from behave import given, then, when

from pages.lobby_page import LobbyPage


@given("I open the global lobby")
def open_lobby(context):
    context.lobby_page = LobbyPage(context.driver)
    context.lobby_page.open()


@when("I enter the lobby with a unique username")
def enter_unique_username(context):
    username = context.lobby_page.unique_username()
    context.lobby_page.join(username)


@then("I should see that I am inside the lobby")
def verify_lobby_entry(context):
    assert context.lobby_page.is_inside()


@given("I open the global lobby for username validation")
def open_lobby_for_validation(context):
    context.lobby_page = LobbyPage(context.driver)
    context.lobby_page.open()


@when("I submit a username containing spaces")
def submit_username_with_spaces(context):
    context.lobby_page.join("invalid username")


@then("the lobby should show the username validation error")
def verify_username_error(context):
    assert (
        context.lobby_page.error_message()
        == "Usa entre 3 y 20 caracteres: letras sin tildes, números, guion o guion bajo."
    )
