from .instances import config
from .web_driver_instance import driver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def click_show_all_categories_button_if_present():
  categories_button_css_selector = ''.join([
    config['groceries_homepage']['categories_container']['css_selector'],
    config['groceries_homepage']['categories_container']['categories_button_appended_css_selector']
  ])

  try:
    # Is "Show ... more" button present?
    driver.find_element(By.CSS_SELECTOR, categories_button_css_selector)

    # Click such present button
    WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable(
        (By.CSS_SELECTOR, categories_button_css_selector)
      )
    ).click()
  except NoSuchElementException:
    raise Exception('No button "Show ... more" found')


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
  is_subcategories_extraction = False, category_name_for_subcategories = ''
) -> list[dict]:
  categories_element_css_selector = ''.join([
    config['groceries_homepage']['categories_container']['css_selector'],
    config['groceries_homepage']['categories_container']['categories_element_appended_css_selector']
  ])

  categories_name_container_css_selector = ''.join([
    config['groceries_homepage']['categories_container']['css_selector'],
    config['groceries_homepage']['categories_container']['categories_name_container_appended_css_selector']
  ])

  categories_elements = driver.find_elements(
    By.CSS_SELECTOR, categories_element_css_selector
  )

  groceries_non_deal_categories = filter_non_deal_categories(
    categories_elements, categories_name_container_css_selector
  )

  url_per_grocery_category = [{} for _ in range(len(groceries_non_deal_categories))]
  for index, grocery_category_dict in enumerate(url_per_grocery_category):
    grocery_category_dict['url'] = (groceries_non_deal_categories[index]
      .find_element(By.CSS_SELECTOR, 'a')
      .get_attribute('href')
    )

    if is_subcategories_extraction:
      grocery_category_dict['grocery_category'] = category_name_for_subcategories
      grocery_category_dict['grocery_subcategory'] = (groceries_non_deal_categories[index]
        .get_attribute('innerText')
      )
    else:
      grocery_category_dict['grocery_category'] = (groceries_non_deal_categories[index]
        .get_attribute('innerText')
      )

  return url_per_grocery_category
