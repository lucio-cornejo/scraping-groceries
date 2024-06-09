from src.instances import config, task_1_2_logger, driver
driver.quit()

from src.subcategories_scraper import save_list_as_JSON
from src.setup_selenium_driver import get_non_wired_driver

import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


PRODUCT_HTML_CONTAINER_PRESENCE_SECONDS_TIMEOUT = config['selenium']['product_html_container_presence_seconds_timeout']

def is_products_page_url_of_paginated_type(products_page_url: str) -> bool:
  non_wired_driver = get_non_wired_driver()
  non_wired_driver.set_page_load_timeout(PRODUCT_HTML_CONTAINER_PRESENCE_SECONDS_TIMEOUT)

  try:
    non_wired_driver.get(products_page_url)
    WebDriverWait(non_wired_driver, PRODUCT_HTML_CONTAINER_PRESENCE_SECONDS_TIMEOUT).until(
      EC.presence_of_element_located(
        (By.CSS_SELECTOR, config['products_website']['product_html_container']['css_selector'])
      )
    )
    return True
  except TimeoutException:
    if '@web/site-top-of-funnel/ProductCardWrapper' in driver.page_source: return True
    return False
  finally:
    non_wired_driver.quit()


if __name__ == '__main__':
  task_1_2_logger.info('Started subtask')

  with open('data/urls_for_task_1.2.json', 'r', encoding = 'utf-8') as f:
    list_products_page_dict = json.loads(f.read())

  paginated_products_page_list_indices = []
  try:
    for index, products_page_dict in enumerate(list_products_page_dict):
      task_1_2_logger.info(f'List index: {index}')

      url = products_page_dict['url']
      if is_products_page_url_of_paginated_type(url):
        paginated_products_page_list_indices.append(index)
      else:
        task_1_2_logger.critical(f'Possible non-paginated type corresponding to URL: {url}')

    # Save filtered JSON with URLs corresponding to paginated products pages
    save_list_as_JSON(
      [list_products_page_dict[i] for i in paginated_products_page_list_indices],
      'data/urls_for_task_2.1.json'
    )
    task_1_2_logger.info('Completed subtask')
  except Exception as e:
    task_1_2_logger.exception(e)
    task_1_2_logger.error('Failed subtask')
