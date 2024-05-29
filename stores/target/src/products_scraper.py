from selenium import webdriver
from selenium.webdriver.common.by import By


def parse_number_of_pages_from_web_text(config: dict, driver: webdriver.Chrome):
  number_of_pages_element_css_selector = ''.join([
    config['products_website']['paginator']['css_selector'],
    config['products_website']['paginator']['number_of_pages_element_appended_css_selector']
  ])

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
    raise Exception('Failed to extract number of pages')
