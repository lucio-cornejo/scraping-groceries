# %%
from src.instances import task_4_2_logger
from src.products_basic_info_extractor import attempt_extraction_of_nested_dict_value

import json
import asyncio
import pandas as pd

# %%
with open(f'data/products_scraped_info_for_task_4.json', 'r', encoding = 'utf-8') as f:
  products_info_json_list = json.loads(f.read())

# %%
len(products_info_json_list)

# %%
products_info_json_list[0]

# %%
async def extract_product_relevant_info(
  product_info: dict, product_dict_index: int
) -> dict:
  print(f'Task started for product index {product_dict_index}')

  relevant_product_info = {}

  """
  Extract product's properties not contained in the list
  product_info["nutrition_facts"]["value_prepared_list"]
  """
  key_name_to_dict_keys_path_mappings = {
    "upc" : "upc",
    "tcin" : "tcin",
    "original_tcin" : "original_tcin",
    "dpci" : "dpci",
    # "path" : "merged_bread_crumbs",
    "merged_bread_crumbs" : "merged_bread_crumbs",
    "title" : "title",
    "url" : "url",
    "image_url" : "image_url",
    "ingredients" : "nutrition_facts;ingredients"
  }

  for key_name, dict_keys_path in key_name_to_dict_keys_path_mappings.items():
    relevant_product_info[key_name] = attempt_extraction_of_nested_dict_value(
      product_info, dict_keys_path
    )

  # Extract relevant product properties
  if not 'nutrition_facts' in product_info.keys(): 
    task_4_2_logger.warning(f'No nutrition_facts for product index {product_dict_index}')
    # return None
    return relevant_product_info
  
  if not 'value_prepared_list' in product_info['nutrition_facts'].keys(): 
    task_4_2_logger.warning(f'No value_prepared_list for product index {product_dict_index}')
    # return None
    return relevant_product_info

  """
  PENDING TO DETERMINE WHICH ITEM FROM nutrition_facts;value_prepared_list
  list should be used to extract nutrition values, because such list has been
  to vary in size, whether 0, 1, 2, even 14, etc .
  """
  if len(product_info['nutrition_facts']['value_prepared_list']) != 1:
    task_4_2_logger.warning(f'List with keys path nutrition_facts;value_prepared_list has length {len(product_info["nutrition_facts"]["value_prepared_list"])} for product index {product_dict_index}')
    return relevant_product_info

  """
  Extract product's properties contained in the first item
  of the list product_info["nutrition_facts"]["value_prepared_list"]
  """
  product_info['nutrition_facts']['value_prepared_list'] = product_info['nutrition_facts']['value_prepared_list'][0]

  key_name_to_dict_keys_path_mappings = {
    "serving_size" : "nutrition_facts;value_prepared_list;serving_size",
    "serving_size_unit_of_measurement" : "nutrition_facts;value_prepared_list;serving_size_unit_of_measurement",
    "servings_per_container" : "nutrition_facts;value_prepared_list;servings_per_container"
  }

  for key_name, dict_keys_path in key_name_to_dict_keys_path_mappings.items():
    relevant_product_info[key_name] = attempt_extraction_of_nested_dict_value(
      product_info, dict_keys_path
    )

  # Assign nutrients columns
  nutrients_dicts_list = attempt_extraction_of_nested_dict_value(
    product_info, "nutrition_facts;value_prepared_list;nutrients"
  )

  if nutrients_dicts_list is None:
    task_4_2_logger.warning(f'No value found for keys path nutrition_facts;value_prepared_list;nutrients, for product index {product_dict_index}')
    return relevant_product_info

  for nutrients_dict in nutrients_dicts_list:
    if nutrients_dict.get('name', False):
      nutrient_name = nutrients_dict['name']

      if nutrients_dict.get('quantity', False):
        relevant_product_info[nutrient_name] = nutrients_dict['quantity']

      if nutrients_dict.get('unit_of_measurement', False):
        relevant_product_info[nutrient_name + '_unit'] = nutrients_dict['unit_of_measurement']

      if nutrients_dict.get('percentage', False):
        relevant_product_info[nutrient_name + '_percentage'] = nutrients_dict['percentage']
    else:
      print(f'No nutrient name for product index {product_dict_index}')

  return relevant_product_info

# %%
async def main():
  print("Main function is running")
  
  tasks = [
    extract_product_relevant_info(
      products_info_json_list[product_index], product_index
    )
    for product_index in range(len(products_info_json_list))
  ]
  
  results = await asyncio.gather(*tasks)
  print("Main function is done")
  return results

# %%
# asyncio.run(main())
products_info_extraction_result = await main()

# %%
"""
# Inspect products' nutrition_facts;value_prepared_lists

def flatten_list(test_list: list) -> list:
  if isinstance(test_list, list):
    tmp_list = []
    for element in test_list:
      tmp_list.extend(flatten_list(element))
    return tmp_list
  else:
    return [test_list]


value_prepared_lists = flatten_list([
  e 
  for e in products_info_extraction_result
  if not e is None
])

values_prepared_df = pd.DataFrame.from_dict(value_prepared_lists)

values_prepared_df["description"].unique().tolist()
"""

# %%
final_dataframe = pd.DataFrame.from_dict(products_info_extraction_result)
final_dataframe

# %%
"""
Assign product properties ignored for task_3_3 
"""
with open(f'data/products_urls_for_task_3.3.json', 'r', encoding = 'utf-8') as f:
  products_basic_info_df = pd.DataFrame.from_dict(json.loads(f.read()))
  
products_basic_info_df

# %%
final_dataframe = final_dataframe.set_index('url')
final_dataframe.update(products_basic_info_df.set_index('url'))
final_dataframe = final_dataframe.reset_index()
final_dataframe

# %%
final_dataframe.shape[0]

# %%
final_dataframe['upc'].isna().sum()

# %%
# Inspect number of missing values per column
(final_dataframe
  .isna().sum()
  .to_frame()
  .reset_index()
  .set_axis(
    ["column_name", 'num_missing_values'], 
    axis = 'columns'
  )
  .sort_values(
    ['num_missing_values', 'column_name'],
    ascending = [True, False]
  )
  .head(40)
)

# %%
pd.set_option('display.max_columns', None)
final_dataframe

# %%
final_dataframe.to_csv('data/final_dataframe.csv', index = False)
