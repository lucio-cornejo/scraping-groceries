# %%
import os; os.chdir('./../')

# %%
from src.instances import task_3_2_logger
from src.ip_rotator import create_gateway_and_session_for_random_IP
from src.products_basic_info_extractor import attempt_extraction_of_nested_dict_value
from src.subcategories_scraper import save_list_as_JSON

from random import randrange
import json
from time import sleep

# %%
task_3_2_logger.info('Started subtask')

# %%
with open('data/unique_products_urls.json', 'r', encoding = 'utf-8') as f:
  GET_request_params_list = json.loads(f.read())
  shared_params = {
    "key" : "9f36aeafbe60771e321a7cc95a78140772ab3e96",
    "pricing_store_id" : "3991",
    "channel" : "WEB"
  }

  GET_request_params_list = [
    {
      **shared_params,
      "tcin": str(product_dict["tcin"]),
      "visitor_id" : f"018EECDE90C702018E5EA8C77C7A746.49747804{randrange(100, 999)}D",
      "page" : f'%2Fp%2FA-{product_dict["tcin"]}'
    }
    for product_dict in GET_request_params_list
  ]

GET_request_params_list

# %%
ENDPOINT_URL = "https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1"
HEADERS = { 
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

# %%
gateway, session = create_gateway_and_session_for_random_IP(ENDPOINT_URL)

GETrequestResults = []
for index, GET_request_params in enumerate(GET_request_params_list):
  print(index)
  
  # if index > 200: break

  rsp = session.get(
    ENDPOINT_URL, 
    headers = HEADERS, 
    params = GET_request_params
  )
  productJSON = rsp.json()
  
  productObject = GET_request_params.copy()

  productTcin = productObject['tcin']
  productItem = None
  try:
    if (attempt_extraction_of_nested_dict_value(productJSON, 'data;product;children')):
      itemWithMatchingTcin = list(filter(
        lambda item: productTcin == item['tcin'],
        productJSON['data']['product']['children']
      ))

      if (len(itemWithMatchingTcin) > 0):
        productItem = itemWithMatchingTcin[0]['item']
      else:
        task_3_2_logger.warn(f'Index {index}: Failed extraction of product children with matching tcin value')
        continue
    else:
      productItem = productJSON['data']['product']['item']

    productObject['nutrition_facts'] = attempt_extraction_of_nested_dict_value(productItem, 'enrichment;nutrition_facts')
    productObject['bullet_descriptions'] = attempt_extraction_of_nested_dict_value(productItem , 'product_description;bullet_descriptions')
    productObject['upc'] = attempt_extraction_of_nested_dict_value(productItem , 'primary_barcode')
    productObject['dpci'] = attempt_extraction_of_nested_dict_value(productItem , 'dpci')
    productObject['origin'] = attempt_extraction_of_nested_dict_value(productItem , 'handling;import_designation_description')
  except:
    task_3_2_logger.warn(f'Index {index}: Failure in some step of product JSON info extraction')
  finally:
    GETrequestResults.append(productObject)
    
    if ((index > 0) and (index % 50 == 0)):
      task_3_2_logger.info(f'Current index: {index}')
      
      save_list_as_JSON(
        GETrequestResults, 'data/unique-products_python.json'
      )

    sleep(randrange(0, 1))

# %%
gateway.shutdown()
