import re

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from .base_page import BasePage


class IMDbPage(BasePage):
    SEARCH_INPUT = (By.ID, "suggestion-search")
    SEARCH_BUTTON = (By.ID, "suggestion-search-button")
    FIRST_RESULT = (By.CSS_SELECTOR, 'a[href*="/title/tt"]')
    RATING = (By.CSS_SELECTOR, '[data-testid="hero-rating-bar__aggregate-rating__score"]')

    def open(self):
        super().open("https://www.imdb.com/")
        if (
            self.driver.title == "403 Forbidden"
            or "awsWafCookieDomainList" in self.driver.page_source
        ):
            raise AssertionError(
                "IMDb mostró una protección anti-bot (403/AWS WAF); "
                "el sitio bloqueó este entorno de automatización."
            )

    def dismiss_consent(self):
        for locator in (
            (By.ID, "onetrust-accept-btn-handler"),
            (By.CSS_SELECTOR, '[data-testid="accept-button"]'),
        ):
            try:
                self.click(locator)
                return
            except TimeoutException:
                continue

    def search(self, title):
        self.dismiss_consent()
        self.type_text(self.SEARCH_INPUT, title)
        self.click(self.SEARCH_BUTTON)

    def open_first_result(self):
        self.click(self.FIRST_RESULT)

    def rating(self):
        text = self.get_text(self.RATING)
        match = re.search(r"\b\d(?:\.\d)?\b", text)
        if not match:
            raise AssertionError(f"IMDb no mostró una calificación numérica: {text!r}")
        return match.group(0)
