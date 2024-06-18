from src.instances import config, task_2_2_logger

from src.ip_rotator import create_gateway_and_session_for_random_IP

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


task_2_2_logger.info('Started subtask')
MAX_NUM_OF_PRODUCTS_TO_FETCH_VIA_GET_REQUEST = config['products_website']['max_number_of_products_to_fetch_via_GET_request']
MAX_OFFSET_VALUE_ACCEPTED_BY_TARGET_API = config['products_website']['max_offset_value_accepted_by_Target_API']

"""
Remove possible duplicates in grocery groups dictionary list,
with respect to the GET request url 
"""
with open('data/get_request_urls_for_task_2.2.json', 'r', encoding = 'utf-8') as f:
  GET_request_urls_data_frame = pd.DataFrame(json.loads(f.read()))

  GET_request_dicts_list = GET_request_urls_data_frame[
    ~GET_request_urls_data_frame.duplicated(subset = ["get_request_url"])
  ].to_dict('records')


def extract_grocery_group_products_basic_info(
  session: requests.Session, index: int, GET_request_url_dict: dict
):
  modified_GET_request_url = change_relevant_string_queries_values(
    GET_request_url_dict['get_request_url'], 
    updated_offset = 0
  )
  task_2_2_logger.info(f'First modified GET request url: {modified_GET_request_url}')

  rsp_json = extract_get_request_json_response(session, modified_GET_request_url)
  if rsp_json is None: raise Exception("Failed extraction of grocery's group products basic info")

  number_of_products = extract_number_of_products(rsp_json)
  if number_of_products is None: raise Exception("Failed extraction of grocery's group products basic info")
  
  task_2_2_logger.info(f'Number of products: {number_of_products}')

  merged_bread_crumbs = merge_bread_crumbs_labels(rsp_json)
  if merged_bread_crumbs is None: 
    task_2_2_logger.critical("Failed extraction of grocery's group path")
    # Assign grocery group path to corresponding value extracted in task-1.2,
    # else, assign None, because in task-3, the grocery group path may be
    # able to be extracted for each product .
    merged_bread_crumbs = GET_request_url_dict.get('grocery_group_path', None)

  products_dicts_list = attempt_extraction_of_nested_dict_value(rsp_json, 'data;search;products')
  if products_dicts_list is None: raise Exception("Failed extraction of grocery's group products basic info")

  group_products_basic_info = []
  for product_dict in products_dicts_list:
    group_products_basic_info.append(extract_products_basic_info(product_dict))

  # Change "offset" url query string parameters to fetch all products' basic info
  if number_of_products > MAX_NUM_OF_PRODUCTS_TO_FETCH_VIA_GET_REQUEST:
    number_of_extra_get_requests = number_of_products // MAX_NUM_OF_PRODUCTS_TO_FETCH_VIA_GET_REQUEST
    task_2_2_logger.info(f'Number of extra GET requests: {number_of_extra_get_requests}')

    for i in range(1, number_of_extra_get_requests + 1):
      updated_offset = i*MAX_NUM_OF_PRODUCTS_TO_FETCH_VIA_GET_REQUEST
      if updated_offset <= MAX_OFFSET_VALUE_ACCEPTED_BY_TARGET_API:
        modified_GET_request_url = change_relevant_string_queries_values(
          GET_request_url_dict['get_request_url'], updated_offset
        )

        rsp_json = extract_get_request_json_response(session, modified_GET_request_url)
        if rsp_json is None: 
          task_2_2_logger.critical(f'Failed GET request JSON extraction at iteration {i}')
          raise Exception("Failed extraction of grocery's group products basic info")

        products_dicts_list = attempt_extraction_of_nested_dict_value(rsp_json, 'data;search;products')
        if products_dicts_list is None: 
          raise Exception("Failed extraction of grocery's group products basic info")
        else:
          for product_dict in products_dicts_list:
            group_products_basic_info.append(extract_products_basic_info(product_dict))
      else:
        task_2_2_logger.critical(f'Updated offset value surpassed its alowed maximum at iteration {i}')
        task_2_2_logger.critical('Completed all valid (offset value wise) extra GET requests')
        break

      if i == number_of_extra_get_requests:
        task_2_2_logger.info('Completed all extra GET requests')

  """
  Save non duplicate data as CSV file
  """
  cat_prods_basic_info_data_frame = pd.DataFrame(group_products_basic_info)

  # Remove duplicate products, via their Target's API 'buy_url' value
  cat_prods_basic_info_data_frame = cat_prods_basic_info_data_frame[
    ~cat_prods_basic_info_data_frame.duplicated(subset = ['url'], keep = 'first')
  ].reset_index(drop = True)

  cat_prods_basic_info_data_frame["merged_bread_crumbs"] = merged_bread_crumbs
  
  where_all_products_extracted = cat_prods_basic_info_data_frame.shape[0] == number_of_products
  if where_all_products_extracted:
    task_2_2_logger.critical("Successful extraction of ALL grocery group's products basic info")
  else:
    task_2_2_logger.critical(f"Failed to extract basic info of {number_of_products - cat_prods_basic_info_data_frame.shape[0]} products")

  task_2_2_logger.critical(f"Found {cat_prods_basic_info_data_frame.isna().sum().sum()} missing values in grocery group's products data frame")

  cat_prods_basic_info_data_frame.to_csv(f'data/csv_files_for_task_3/index_{index}.csv', index = False)
  task_2_2_logger.critical('Completed local storage of data frame')


if __name__ == '__main__':
  gateway = None
  gateway_session = None

  was_IP_banned = True
  max_number_of_IP_rotation_attempts = 3

  for index in range(len(GET_request_dicts_list)):
    task_2_2_logger.info('\n')
    task_2_2_logger.info(f'GET_request_dicts list index: {index}')

    attempt_number = 1
    while attempt_number <= max_number_of_IP_rotation_attempts:
      if was_IP_banned:
        gateway, gateway_session = create_gateway_and_session_for_random_IP(
          GET_request_dicts_list[index]['get_request_url']
        )

      try:
        extract_grocery_group_products_basic_info(
          gateway_session, index, GET_request_dicts_list[index]
        )
        was_IP_banned = False
        break
      except Exception as e:
        was_IP_banned = True
        attempt_number += 1

        task_2_2_logger.critical('IP ADDRESS MAY HAVE BEEN BANNED BY TARGET')
        task_2_2_logger.exception(e)

        gateway.shutdown()

  gateway.shutdown()

  task_2_2_logger.info('Completed subtask')
