from src.instances import config, task_2_1_logger, driver

import json
import pandas as pd


task_2_1_logger.info('Started subtask')
with open('data/urls_for_task_2.1.json', 'r', encoding = 'utf-8') as f:
  grocery_groups_data_frame = pd.DataFrame(json.loads(f.read()))

  # Include in GET request url search, those URLs for which the test 
  # for paginated products webpage failed to assign a boolean .
  grocery_groups_data_frame["is_website_possibly_paginated"] = grocery_groups_data_frame["is_website_possibly_paginated"].fillna(True)

  task_2_1_logger.info(f'Number of URLs assigned as possibly not-paginated: {(grocery_groups_data_frame["is_website_possibly_paginated"] == False).sum()}\n')

  # Assemble grocery groups labels
  grocery_groups_data_frame["grocery_group"]  = (
    grocery_groups_data_frame["grocery_category"] +
    grocery_groups_data_frame["grocery_subcategory"].apply(lambda x: '/' + x if not pd.isna(x) else '')
  )

  # Remove URL duplicates and keep only the grocery group label and URL
  grocery_groups_data_frame = grocery_groups_data_frame[~grocery_groups_data_frame.duplicated(subset = ['url'])]
  grocery_groups_dicts = (grocery_groups_data_frame
    [grocery_groups_data_frame["is_website_possibly_paginated"]]
    [["grocery_group", "url", "grocery_group_path"]]
    .to_dict('records')
  )


PRODUCTS_BASIC_INFO_PATTERN_URL ="https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2"

def find_products_basic_info_get_request_url(grocery_group_dict: dict):
  category_url = grocery_group_dict['url']
  
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
  
  grocery_group_dict['get_request_url'] = products_basic_info_get_request[0].url
  task_2_1_logger.info(f'{products_basic_info_get_request[0].url}\n')


if __name__ == '__main__':
  try:
    for index, grocery_group_dict in enumerate(grocery_groups_dicts):
      task_2_1_logger.info(f'List index, category url: {index}, {grocery_group_dict["url"]}')
      find_products_basic_info_get_request_url(grocery_group_dict)

      del driver.requests
    
    with open('data/get_request_urls_for_task_2.2.json', 'w', encoding = 'utf-8') as f:
      json.dump(grocery_groups_dicts, f, ensure_ascii = False, indent = 2)

    task_2_1_logger.info('Completed subtask')
  except Exception as e:
    task_2_1_logger.exception(e)
