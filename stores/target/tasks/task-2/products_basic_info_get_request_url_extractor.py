from src.instances import config, driver

import json

# Create list where each element contains an url for Selenium,
# from which's website the products' basic info will be extracted
with open('data/initial_urls_for_task_2.json', 'r', encoding = 'utf-8') as f:
  list_categories_products_url_dict = json.loads(f.read())

PRODUCTS_BASIC_INFO_PATTERN_URL ="https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2"

def extract_products_basic_info_get_request_relevant_data(categories_products_url_dict: dict):
  del driver.requests
  driver.get(categories_products_url_dict['url'])
  driver.wait_for_request(
    PRODUCTS_BASIC_INFO_PATTERN_URL, 
    timeout = config['selenium']['products_basic_info_get_request_seconds_timeout']
  )

  products_basic_info_get_request = list(filter(
    lambda request: PRODUCTS_BASIC_INFO_PATTERN_URL in request.url,
    driver.requests
  ))
  if len(products_basic_info_get_request) > 1:
    raise Exception("More than one request matched the url pattern")
  
  categories_products_url_dict['get_request_url'] = products_basic_info_get_request[0].url


if __name__ == '__main__':
  for categories_products_url_dict in list_categories_products_url_dict:
    try:
      extract_products_basic_info_get_request_relevant_data(categories_products_url_dict)
    except:
      continue

  with open('./data/get_request_urls_for_task_2.json', 'w', encoding = 'utf-8') as f:
    json.dump(list_categories_products_url_dict, f, ensure_ascii = False, indent = 2)
