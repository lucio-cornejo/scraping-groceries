# %%
import os; os.chdir('./../../../')

# %%
from src.instances import task_4_1_logger
from src.products_json_to_dataframe_converter import convert_product_info_to_single_row_data_frame

import os
import json
import asyncio
import pandas as pd

# %%
groups_jsons = list(map(
  lambda path: 'data/' + path,
  list(filter(
    lambda path: path.startswith('group-products-info-index'),
    os.listdir('data/')
  ))
))

len(groups_jsons)

# %%
group_products_list = []

for groups_json_path in groups_jsons:
  with open(groups_json_path, 'r', encoding = 'utf-8') as f:
    group_products_dicts_list = json.loads(f.read())

  group_products_list = [
    *group_products_list,
    *group_products_dicts_list
  ]

# %%
len(group_products_list)

# %%
async def convert_product_dict_to_df(
  product_dict: dict, product_dict_index: int
):
  task_4_1_logger.info(f'Task started for product index {product_dict_index}')
  
  return convert_product_info_to_single_row_data_frame(
    product_dict, row_index = 0
  )

# %%
async def main():
  print("Main function is running")
  
  tasks = [
    convert_product_dict_to_df(
      group_products_list[product_index], product_index
    )
    for product_index in range(len(group_products_list))
  ]
  
  results = await asyncio.gather(*tasks)
  print("Main function is done")
  return results

# %%
# asyncio.run(main())
products_info_extractions_results = await main()

# %%
products_info_extractions_results[-1]

# %%
final_dataframe = pd.DataFrame()

for product_single_row_dataframe in products_info_extractions_results:
  final_dataframe = pd.concat(
    [final_dataframe, product_single_row_dataframe],
    ignore_index = True
  )

final_dataframe
# %%
products_info_extractions_results

# %%
final_dataframe = pd.DataFrame.from_dict(products_info_extractions_results)
final_dataframe.to_csv('data/final_dataframe.csv', index = False)

# %%
pd.set_option('display.max_columns', None)
final_dataframe

# %%
final_dataframe.shape[0]

# %%
final_dataframe['upc'].isna().sum()
# %%