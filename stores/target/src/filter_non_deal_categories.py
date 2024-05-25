from selenium.webdriver.common.by import By


def is_category_text_from_deal_element(category_text: str):
  return category_text.lower().endswith('deals')

def filter_non_deal_categories(
  categories_web_elements: list, 
  categories_name_element_css_selector: str
) -> list:
  categories = categories_web_elements.copy()

  # Assume only one category is for deals
  deals_category_element_index = list(map(
    lambda category_element: is_category_text_from_deal_element(
      category_element
        .find_element(By.CSS_SELECTOR, categories_name_element_css_selector)
        .get_attribute('innerText')
    ),
    categories
  )).index(True)

  # Remove deals category
  categories.pop(deals_category_element_index)

  return categories
