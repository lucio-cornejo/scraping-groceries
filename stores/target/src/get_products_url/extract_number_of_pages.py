from selenium import webdriver
from selenium.webdriver.common.by import By


def try_parsing_number_of_pages_from_web_text(
  driver: webdriver.Chrome, 
  number_of_pages_element_css_selector: str
):
  try:
    number_of_pages_element = driver.find_element(
      By.CSS_SELECTOR, number_of_pages_element_css_selector
    )
    return int(
      # Expected text example: "Page 1 of 12"
      number_of_pages_element
        .get_attribute('innerText')
        .strip()
        .split('of ')
        [-1]
    )
  except:
    return None
