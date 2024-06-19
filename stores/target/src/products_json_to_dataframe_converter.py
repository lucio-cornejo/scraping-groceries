from .instances import task_4_1_logger

from .products_basic_info_extractor import attempt_extraction_of_nested_dict_value

import pandas as pd


def convert_product_info_to_single_row_data_frame(
  product_info: dict, row_index: int
# ) -> pd.DataFrame:
) -> dict:
  # product_single_row_df = pd.DataFrame(index = [row_index])
  product_single_row_df = {}

  try:
    # Extract item from list which is expected to contain a single 
    # element, due to containing the label info of the product for
    # which there was a tcin match. 
    # The case where such list has more than one element, which is 
    # expected to not exist, may be due to presenting the product's
    # label info in different units (for example, Kcal instead of cal)
    product_info['nutrition_facts']['value_prepared_list'] = product_info['nutrition_facts']['value_prepared_list'][0]

    """
    Assign columns via simple nested dictionary mappings
    """
    column_name_to_dict_keys_path_mappings = {
      "upc" : "upc",
      "tcin" : "tcin",
      "original_tcin" : "original_tcin" ,
      "dpci" : "dpci" ,
      "title" : "title",
      "url" : "url",
      "image_url" : "image_url",
      "path" : "merged_bread_crumbs",
      "ingredients" : "nutrition_facts;ingredients",
      "serving_size" : "nutrition_facts;value_prepared_list;serving_size",
      "serving_size_unit_of_measurement" : "nutrition_facts;value_prepared_list;serving_size_unit_of_measurement",
      "servings_per_container" : "nutrition_facts;value_prepared_list;servings_per_container"
    }

    for column_name, dict_keys_path in column_name_to_dict_keys_path_mappings.items():
      product_single_row_df[column_name] = attempt_extraction_of_nested_dict_value(
        product_info, dict_keys_path
      )

    """
    Assign nutrients columns
    """
    nutrients_dicts_list = attempt_extraction_of_nested_dict_value(
      product_info, "nutrition_facts;value_prepared_list;nutrients"
    )

    for nutrients_dict in nutrients_dicts_list:
      column_name = nutrients_dict['name']

      if nutrients_dict.get('quantity', False):
        product_single_row_df[column_name] = nutrients_dict['quantity']

      if nutrients_dict.get('unit_of_measurement', False):
        product_single_row_df[column_name + '_unit'] = nutrients_dict['unit_of_measurement']

      if nutrients_dict.get('percentage', False):
        product_single_row_df[column_name + '_percentage'] = nutrients_dict['percentage']
  except Exception as e:
    task_4_1_logger.error(e)
  finally:
    return product_single_row_df
