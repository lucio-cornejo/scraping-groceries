from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def click_show_all_categories_button_if_present(
  driver: webdriver.Chrome,
  categories_button_css_selector: str
):
  try:
    # Is "Show ... more" button present?
    driver.find_element(
      By.CSS_SELECTOR, categories_button_css_selector
    )

    # Click such present button
    WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable(
        (By.CSS_SELECTOR, categories_button_css_selector)
      )
    ).click()
  except NoSuchElementException:
    raise Exception('No button "Show ... more" found')
