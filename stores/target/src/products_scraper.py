from .instances import config, task_two_logger, driver

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


def load_all_products_in_page():
  actions = ActionChains(driver)
  for _ in range(5):
    actions.send_keys(Keys.END).perform()
    time.sleep(0.5)

    for _ in range(10):
      actions.send_keys(Keys.PAGE_UP).perform()
      time.sleep(0.1)


def is_products_website_paginated():
  try:
    driver.find_element(
      By.CSS_SELECTOR, config['products_website']['paginator']['css_selector']
    )
    return True
  except NoSuchElementException:
    return False


def parse_number_of_pages_from_web_text():
  number_of_pages_element_css_selector = ''.join([
    config['products_website']['paginator']['css_selector'],
    config['products_website']['paginator']['number_of_pages_element_appended_css_selector']
  ])

  try:
    number_of_pages_element = driver.find_element(
      By.CSS_SELECTOR, number_of_pages_element_css_selector
    )
    return int(
      # Expected text example: "page 1 of 12"
      number_of_pages_element
        .get_attribute('innerText')
        .strip()
        .split('of ')
        [-1]
    )
  except Exception as e:
    task_two_logger.exception('Failed to extract number of pages')
    raise e


def click_next_page_in_products_website():
  next_page_button_css_selector = ''.join([
    config['products_website']['paginator']['css_selector'],
    config['products_website']['paginator']['next_page_element_appended_css_selector']
  ])

  try:
    driver.find_element(By.CSS_SELECTOR, next_page_button_css_selector)
    driver.execute_script(f"""
      document.querySelector("{next_page_button_css_selector}").click();
    """)
  except Exception as e:
    task_two_logger.exception('Failed to click "Next page" button')
    raise e


def extract_products_url_and_image_url(
  grocery_category: str, grocery_subcategory: str
) -> list[dict]:
  javascript_code_template_for_products_info_assembly = """
    const products = Array.from(
      document.querySelectorAll("{product_html_container_css_selector}")
    );

    return products.map(product => {{
      const product_info = {{}};

      product_info["grocery_category"] = "{grocery_category}";
      product_info["grocery_subcategory"] = {grocery_subcategory};

      // Extract product's url and image url
      product_info["title"] = product.querySelector("{product_title_html_anchor_css_selector}").innerText;
      product_info["url"] = product.querySelector("{product_url_html_anchor_css_selector}").href;
      product_info["image_url"] = product.querySelector("{product_image_html_img_css_selector}").src;

      return product_info;
    }})
  """

  return driver.execute_script(
    javascript_code_template_for_products_info_assembly.format(
      product_html_container_css_selector = config['products_website']['product_html_container']['css_selector'],
      grocery_category = grocery_category,
      grocery_subcategory = "null" if grocery_subcategory is None else grocery_subcategory,
      product_title_html_anchor_css_selector = config['products_website']['product_html_container']['product_title_html_anchor_css_selector'],
      product_url_html_anchor_css_selector = config['products_website']['product_html_container']['product_url_html_anchor_css_selector'],
      product_image_html_img_css_selector = config['products_website']['product_html_container']['product_image_html_img_css_selector']
    )
  )
