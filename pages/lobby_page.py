import uuid

from selenium.webdriver.common.by import By

from .base_page import BasePage


class LobbyPage(BasePage):
    USERNAME = (By.ID, "username")
    JOIN_BUTTON = (By.ID, "btn-login")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "p.error-message[role='alert']")
    LOBBY_TEXT = (By.XPATH, "//*[contains(normalize-space(), 'Estás dentro como')]")

    def open(self):
        super().open("https://lobby-global.vercel.app/")

    def unique_username(self):
        return f"User{uuid.uuid4().hex[:12]}"

    def join(self, username):
        self.type_text(self.USERNAME, username)
        self.click(self.JOIN_BUTTON)

    def error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def is_inside(self):
        return self.is_displayed(self.LOBBY_TEXT)
