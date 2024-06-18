# %%
import os; os.chdir('./../../../')

# %%
from src.instances import task_3_3_logger
from src.ip_rotator import create_gateway_and_session_for_random_IP
from src.products_basic_info_extractor import attempt_extraction_of_nested_dict_value
from src.subcategories_scraper import save_list_as_JSON

from random import randrange
import json
from time import sleep
import asyncio

# %%
task_3_3_logger.info('Started subtask')

# %%
"""
Assemble parameters for each GET request
"""
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
"""
Divide list of GET request params into sublists of at most
150 elements, that is, the number of GET requests, per IP,
that Target's API seems to allow for free, before temporary IP ban
"""
group_size = 150
number_of_products = len(GET_request_params_list)

# Perform modulo operation in Python
remainder = ((number_of_products % group_size) + group_size) % group_size

indices_of_groups_first_item = [
  group_size * e for e in range(1 + (number_of_products - remainder - group_size) // group_size)
]

indices_per_group = [
  [index_shift + first_group_item_index for index_shift in range(group_size)]
  for first_group_item_index in indices_of_groups_first_item
]

# Add possibly pending indices to array of groups items indices
if remainder != 0:
  indices_per_group.append([
    index_shift + number_of_products - remainder for index_shift in range(remainder)
  ])

grouped_products_array = [
  [GET_request_params_list[index] for index in group_items_indices]
  for group_items_indices in indices_per_group
]

grouped_products_array

# %%
grouped_products_array[0]

# %%
print(len(grouped_products_array))
list(map(len, grouped_products_array))

# %%
"""
Create API Gateway session based on Target's API "endpoint" url
for product info extraction
"""
ENDPOINT_URL = "https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1"
HEADERS = { 
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

gateway, session = create_gateway_and_session_for_random_IP(ENDPOINT_URL)

# %%
async def extract_group_products_info(
  params_group: list[dict], group_index: int
):
  task_3_3_logger.info(f"Started execution for group index {group_index}")

  GETrequestResults = []
  for index, product_params in enumerate(params_group):
    rsp = session.get(
      ENDPOINT_URL, 
      headers = HEADERS, 
      params = product_params
    )
    productJSON = rsp.json()
    
    productObject = product_params.copy()

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
          task_3_3_logger.warning(f'Tcin {productTcin}: Failed extraction of product children with matching tcin value')
          continue
      else:
        productItem = productJSON['data']['product']['item']

      productObject['nutrition_facts'] = attempt_extraction_of_nested_dict_value(productItem, 'enrichment;nutrition_facts')
      productObject['bullet_descriptions'] = attempt_extraction_of_nested_dict_value(productItem , 'product_description;bullet_descriptions')
      productObject['upc'] = attempt_extraction_of_nested_dict_value(productItem , 'primary_barcode')
      productObject['dpci'] = attempt_extraction_of_nested_dict_value(productItem , 'dpci')
      productObject['origin'] = attempt_extraction_of_nested_dict_value(productItem , 'handling;import_designation_description')
    except Exception as e:
      task_3_3_logger.warning(f'Tcin {productTcin}: Failure in some step of product JSON info extraction')
      task_3_3_logger.exception(e)
    finally:
      GETrequestResults.append(productObject)
      
      if ((index > 0) and (index % 50 == 0)):
        save_list_as_JSON(
          GETrequestResults, 
          f'data/group-products-info-index-{group_index}.json'
        )

      sleep(randrange(0, 1))

  return GETrequestResults


# %%
async def main():
  print("Main function is running")
  
  tasks = [
    extract_group_products_info(
      grouped_products_array[group_index], group_index
    )
    for group_index in range(len(grouped_products_array))
  ]
  
  results = await asyncio.gather(*tasks)
  print("Main function is done")
  return results

# %%
# asyncio.run(main())
products_info_extractions_results = await main()

# %%
gateway.shutdown()
