from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def is_category_text_from_deal_element(category_text: str):
  return category_text.lower().endswith('deals')


def filter_non_deal_categories(
  categories_web_elements: list, 
  categories_name_element_css_selector: str
) -> list:
  categories = categories_web_elements.copy()

  # Assume only one category is for deals
  is_category_a_deal_case = list(map(
    lambda category_element: is_category_text_from_deal_element(
      category_element
        .find_element(By.CSS_SELECTOR, categories_name_element_css_selector)
        .get_attribute('innerText')
    ),
    categories
  ))

  # Remove deal category if found
  if True in is_category_a_deal_case:
    categories.pop(is_category_a_deal_case.index(True))

  return categories


def extract_categories_name_and_url(
  driver: webdriver.Chrome,
  categories_element_css_selector: str,
  categories_name_container_css_selector: str
) -> list[dict]:
  categories_elements = driver.find_elements(
    By.CSS_SELECTOR, categories_element_css_selector
  )

  groceries_non_deal_categories = filter_non_deal_categories(
    categories_elements, categories_name_container_css_selector
  )

  url_per_grocery_category = [{} for _ in range(len(groceries_non_deal_categories))]
  for index, grocery_category_dict in enumerate(url_per_grocery_category):
    grocery_category_dict['grocery_category'] = (groceries_non_deal_categories[index]
      .get_attribute('innerText')
    )
    grocery_category_dict['url'] = (groceries_non_deal_categories[index]
      .find_element(By.CSS_SELECTOR, 'a')
      .get_attribute('href')
    )

  return  url_per_grocery_category
