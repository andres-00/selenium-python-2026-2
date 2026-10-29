from behave import given, then, when

from pages.imdb_page import IMDbPage


@given("I open IMDb home")
def open_imdb(context):
    context.imdb_page = IMDbPage(context.driver)
    context.imdb_page.open()


@when('I search IMDb for "{title}" and open the first result')
def search_imdb(context, title):
    context.imdb_page.search(title)
    context.imdb_page.open_first_result()


@then("the movie page should show a numeric rating")
def verify_imdb_rating(context):
    rating = context.imdb_page.rating()
    assert rating.replace(".", "", 1).isdigit()
