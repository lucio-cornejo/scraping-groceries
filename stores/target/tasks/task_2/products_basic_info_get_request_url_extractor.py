from src.instances import config, task_2_1_logger, driver

import json
import pandas as pd


"""
Remove duplicate url items of list from which URLs will be extracted
for fetching the products' basic info, per category/subcategory 
"""
with open('data/urls_for_task_2.1.json', 'r', encoding = 'utf-8') as f:
  df = pd.DataFrame(json.loads(f.read())).fillna(pd.NA)
  list_categories_products_url_dict = df[~df.duplicated(subset = ['url'])].to_dict('records')


PRODUCTS_BASIC_INFO_PATTERN_URL ="https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2"

def find_products_basic_info_get_request_url(categories_products_url_dict: dict):
  category_url = categories_products_url_dict['url']
  
  del driver.requests
  driver.get(category_url)
  driver.wait_for_request(
    PRODUCTS_BASIC_INFO_PATTERN_URL, 
    timeout = config['selenium']['products_basic_info_get_request_seconds_timeout']
  )

  products_basic_info_get_request = list(filter(
    lambda request: PRODUCTS_BASIC_INFO_PATTERN_URL in request.url,
    driver.requests
  ))

  if len(products_basic_info_get_request) > 1:
    raise Exception(f"More than one request matched the url pattern for url {category_url}")
  
  categories_products_url_dict['get_request_url'] = products_basic_info_get_request[0].url
  task_2_1_logger.critical(products_basic_info_get_request[0].url)


if __name__ == '__main__':
  task_2_1_logger.info('Started URLs extraction')
  
  for index, categories_products_url_dict in enumerate(list_categories_products_url_dict):
    task_2_1_logger.info(f'List index, category url: {index}, {categories_products_url_dict["url"]}')
    try:
      find_products_basic_info_get_request_url(categories_products_url_dict)
    except Exception as e:
      task_2_1_logger.exception(e)

      del driver.requests
      continue

  with open('data/get_request_urls_for_task_2.2.json', 'w', encoding = 'utf-8') as f:
    json.dump(list_categories_products_url_dict, f, ensure_ascii = False, indent = 2)

  task_2_1_logger.info('Completed subtask')
