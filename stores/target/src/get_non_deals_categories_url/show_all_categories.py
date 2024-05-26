from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def click_show_all_categories_button(
  driver: webdriver.Chrome,
  categories_button_css_selector: str
):
  WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
      (By.CSS_SELECTOR, categories_button_css_selector)
    )
  ).click()
