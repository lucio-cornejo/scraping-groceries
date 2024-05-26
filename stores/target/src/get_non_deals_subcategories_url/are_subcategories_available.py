from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def are_subcategories_available(
  driver: webdriver.Chrome,
  category_url: str,
  categories_container_css_selector: str
) -> bool:
  driver.get(category_url)

  try:
    driver.find_element(
      By.CSS_SELECTOR, categories_container_css_selector
    )
    return True
  except NoSuchElementException:
    return False
