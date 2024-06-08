from src.instances import task_2_2_logger

import requests
from random import randrange


def change_relevant_string_queries_values(GET_request_url: str, updated_offset: int) -> str:
  string_queries = GET_request_url.split('&')

  for index, string_query in enumerate(string_queries):
    if string_query.startswith('count='):
      # Change maximum number of products retrieved in GET request
      # to maximum value accepted by the GET request "endpoint" .
      string_queries[index] = 'count=28'
    
    if string_query.startswith('offset='):
      string_queries[index] = f'offset={updated_offset}'
    
    if string_query.startswith('visitor_id='):
      random_three_digit_integer = randrange(100, 999)
      string_queries[index] = f'visitor_id=018FF5C67E2502018598DB5AB7270{random_three_digit_integer}'

  return '&'.join(string_queries)


def extract_get_request_json_response(session_object: requests.Session, get_request_url: str) -> dict|None:
  response = session_object.get(
    get_request_url,
    headers = { 
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
  )
  
  if response.status_code == 200: return response.json()
  
  task_2_2_logger.critical('Failed GET request JSON extraction')
  return None


def extract_number_of_products(response_json: dict) -> int|None:
  try:
    return response_json["data"]["search"]["search_response"]["metadata"]["total_results"]
  except:
    task_2_2_logger.critical('Failed extraction of number of products')
    return None


def merge_bread_crumbs_labels(response_json: dict) -> str|None:
  try:
    bread_crumb_list = [
      dictionary 
      for dictionary in response_json["data"]["search"]["search_response"]["bread_crumb_list"]
      if 'values' in dictionary.keys()
    ]
    
    if len(bread_crumb_list) != 1: raise Exception("Expected a list of length 1")

    bread_crumb_list = bread_crumb_list[0]['values']
    # Separate each bread crumb by '/' character
    return '/'.join([bread_crumb['label'] for bread_crumb in bread_crumb_list])
  except:
    task_2_2_logger.critical('Failed bread crumbs extraction')
    return None


def attempt_extraction_of_nested_dict_value(dictionary: dict, dict_keys_sequence_string: str):
  """
  @param dict_keys_sequence_string: String of the form
    'key1;key2;...;keyN' in order to extract the value
    dictionary['key1']['key2'][...]['keyN'], if it exists 
  """
  keys_sequence = dict_keys_sequence_string.split(';')
  try:
    searched_value = dictionary[keys_sequence[0]]
    if len(keys_sequence) == 1: return searched_value
    
    for dict_key in keys_sequence[1:]:
      searched_value = searched_value[dict_key]
    return searched_value
  except:
    # task_2_2_logger.critical(f'Failed nested dictionary value extraction for keys sequence {dict_keys_sequence_string}')
    return None


def extract_products_basic_info(response_json_data_search_product: dict) -> dict:
  info_name__mapping__keys_sequence = {
    'tcin' : 'tcin',
    'original_tcin' : 'original_tcin',
    'dpci' : 'item;dpci',
    'title' : 'item;product_description;title',
    'url' : 'item;enrichment;buy_url',
    'image_url' : 'item;enrichment;images;primary_image_url'
  }

  product_basic_info = {}
  for info_key, keys_sequence in info_name__mapping__keys_sequence.items():
    product_basic_info[info_key] = attempt_extraction_of_nested_dict_value(
      response_json_data_search_product, keys_sequence
    )

  return product_basic_info
