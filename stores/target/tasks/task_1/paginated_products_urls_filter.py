from src.instances import config, task_1_2_logger, driver
driver.quit()

from src.subcategories_scraper import save_list_as_JSON

import json
import requests


HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
EXPECTED_STRING_IN_PAGINATED_PRODUCTS_PAGE_HTML = config['expected_string_in_paginated_products_page_html']

def is_products_page_url_of_paginated_type(session: requests.Session, products_page_url: str) -> bool:
  response = session.get(products_page_url)
  response = session.get(products_page_url, headers = HEADERS)
  if response.status_code == 200:
    return EXPECTED_STRING_IN_PAGINATED_PRODUCTS_PAGE_HTML in response.text
    
  raise Exception(f'Failed GET request, with status code {response.status_code}')



if __name__ == '__main__':
  task_1_2_logger.info('Started subtask')

  with open('data/urls_for_task_1.2.json', 'r', encoding = 'utf-8') as f:
    list_products_page_dict = json.loads(f.read())

  paginated_products_page_list_indices = [] 
  try:
    session = requests.Session()

    for index, products_page_dict in enumerate(list_products_page_dict):
      task_1_2_logger.info(f'List index: {index}')

      url = products_page_dict['url']
      if is_products_page_url_of_paginated_type(session, url):
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
