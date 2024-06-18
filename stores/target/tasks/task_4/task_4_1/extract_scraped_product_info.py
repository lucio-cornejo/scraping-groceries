# %%
from src.instances import task_4_1_logger
from src.products_json_to_dataframe_converter import convert_product_info_to_single_row_data_frame

import os
import json
import asyncio

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
with open(groups_jsons[0], 'r', encoding = 'utf-8') as f:
  group_products_list = json.loads(f.read())

group_products_list

# %%
async def convert_product_dict_to_df(
  product_dict: dict, product_dict_index: int
):
  task_4_1_logger.info(f'Task starte for product index {product_dict_index}')
  
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
