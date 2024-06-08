# %%
from src.instances import task_2_2_logger

from src.products_basic_info_extractor import (
  extract_get_request_json_response,
  extract_number_of_products,
  merge_bread_crumbs_labels,
  attempt_extraction_of_nested_dict_value,
  extract_products_basic_info,
  change_relevant_string_queries_values
)

import json
import pandas as pd
import requests


# %%
with open('data/get_request_urls_for_task_2.2.json', 'r', encoding = 'utf-8') as f:
  GET_request_urls_data_frame = pd.DataFrame(json.loads(f.read()))

  GET_request_urls_dict = GET_request_urls_data_frame[
    ~GET_request_urls_data_frame.duplicated(subset = ["get_request_url"])
  ].to_dict('records')

GET_request_urls_dict

# %%
for index, GET_request_url_dict in enumerate(GET_request_urls_dict):
  session = requests.Session()
  modified_GET_request_url = change_relevant_string_queries_values(
    GET_request_url_dict['get_request_url'], 
    updated_offset = 0
  )

  rsp_json = extract_get_request_json_response(session, modified_GET_request_url)
  if rsp_json is None: break

  number_of_products = extract_number_of_products(rsp_json)
  if number_of_products is None: break
  
  task_2_2_logger.info(f'Number of products: {number_of_products}')

  merged_bread_crumbs = merge_bread_crumbs_labels(rsp_json)
  if merged_bread_crumbs is None: break

  products_dicts_list = attempt_extraction_of_nested_dict_value(rsp_json, 'data;search;products')
  if products_dicts_list is None: break

  category_products_basic_info = []
  for product_dict in products_dicts_list:
    category_products_basic_info.append(extract_products_basic_info(product_dict))

  
  if number_of_products > 28:
    n = number_of_products // 28
    for i in range(1, n + 1):
      updated_offset = i*28
      task_2_2_logger.info(f'Started new iteration with offset {updated_offset}')
      
      modified_GET_request_url = change_relevant_string_queries_values(
        GET_request_url_dict['get_request_url'], updated_offset
      )

      rsp_json = extract_get_request_json_response(session, modified_GET_request_url)
      if rsp_json is None: 
        task_2_2_logger.critical(f'Failed GET request JSON extraction at iteration {i}')
        break

      products_dicts_list = attempt_extraction_of_nested_dict_value(rsp_json, 'data;search;products')
      if products_dicts_list is None: 
        break
      else:
        for product_dict in products_dicts_list:
          category_products_basic_info.append(extract_products_basic_info(product_dict))



  break

category_products_basic_info

# %%
cat_prods_basic_info_data_frame = pd.DataFrame(category_products_basic_info)

# Remove duplicate products, via their Target's API 'buy_url' value
cat_prods_basic_info_data_frame = cat_prods_basic_info_data_frame[
  ~cat_prods_basic_info_data_frame.duplicated(subset = ['url'], keep = 'first')
].reset_index(drop = True)

cat_prods_basic_info_data_frame["merged_bread_crumbs"] = merged_bread_crumbs
cat_prods_basic_info_data_frame

# %%
cat_prods_basic_info_data_frame.shape[0] == number_of_products

# %%
0 == cat_prods_basic_info_data_frame.isna().sum().sum()
