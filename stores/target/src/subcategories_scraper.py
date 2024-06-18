from .instances import config
from .web_driver_instance import driver

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


def save_list_as_JSON(urls_per_page_to_scrap: list[dict], file_path: str):
  with open(f'{file_path}', 'w', encoding = 'utf-8') as f:
    dump(urls_per_page_to_scrap, f, ensure_ascii = False, indent = 2)


def extract_category_subcategories_urls(products_cat_or_subcat_dict: dict, is_subcategory = False) -> list[dict]:
  if not 'subcategories' in products_cat_or_subcat_dict.keys():
    if is_subcategory: return products_cat_or_subcat_dict
  
    return [products_cat_or_subcat_dict]
  
  return list(map(
    lambda subcategory_dict: extract_category_subcategories_urls(subcategory_dict, True),
    products_cat_or_subcat_dict['subcategories']
  ))


def flatten_list_of_categories_and_subcategories_url(categories_and_subcategories_url_list: list[dict]) -> list[dict]:
  list_of_lists = list(map(extract_category_subcategories_urls, categories_and_subcategories_url_list))
  return [x for sub_list in list_of_lists for x in sub_list]
