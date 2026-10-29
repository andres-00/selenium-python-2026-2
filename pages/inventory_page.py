from selenium.webdriver.common.by import By
from .base_page import BasePage

class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, 'inventory_list')

    def is_inventory_page_displayed(self):
        return self.find_element(self.TITLE).is_displayed()

    def add_product_to_cart(self, product_name):
        product_xpath = f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']//button"
        self.driver.find_element(By.XPATH, product_xpath).click()

    def get_cart_count(self):
        return self.get_text((By.CLASS_NAME, "shopping_cart_badge"))
