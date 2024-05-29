from .instances import config, driver

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from json import dump


def are_subcategories_available(category_url: str) -> bool:
  driver.get(category_url)

  categories_container_css_selector = config['groceries_homepage']['categories_container']['css_selector']
  try:
    driver.find_element(By.CSS_SELECTOR, categories_container_css_selector)
    return True
  except NoSuchElementException:
    return False


def save_list_of_urls_per_page_to_scrap(urls_per_page_to_scrap: list[dict], file_path: str):
  with open(f'{file_path}', 'w', encoding = 'utf-8') as f:
    dump(urls_per_page_to_scrap, f, ensure_ascii = False, indent = 2)
