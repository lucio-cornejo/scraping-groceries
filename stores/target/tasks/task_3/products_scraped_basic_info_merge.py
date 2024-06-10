from src.instances import task_3_1_logger

import os
import json
import pandas as pd


if __name__ == '__main__':
  task_3_1_logger.info('Started subtask')
  
  """
  Were CSV files created for all unique GET request urls?
  """
  folder_csv_files_for_task_3 = 'data/csv_files_for_task_3'
  csv_files_for_task_3 = list(map(
    lambda file_name: folder_csv_files_for_task_3 + '/' + file_name,
    os.listdir(folder_csv_files_for_task_3)
  ))

  with open('data/get_request_urls_for_task_2.2.json', 'r', encoding = 'utf-8') as f:
    GET_request_urls_data_frame = pd.DataFrame(json.loads(f.read()))

    GET_request_urls_data_frame = GET_request_urls_data_frame[
      ~GET_request_urls_data_frame.duplicated(subset = ["get_request_url"])
    ].reset_index(drop = True)


  if len(csv_files_for_task_3) == GET_request_urls_data_frame.shape[0]:
    task_3_1_logger.info('Successful CSV file creation for all unique GET request urls')
  else:
    task_3_1_logger.warning(f'Failed to create CSV files for {GET_request_urls_data_frame.shape[0] - len(csv_files_for_task_3)} unique GET request urls')


  """
  Merge products' basic info data, stored in CSV files, 
  into single CSV, after removing duplicate URLs of products,
  due to some products being accessible through different
  grocery groups (categories/subcategories/special offers) .
  """
  extracted_products_basic_info_data_frame = pd.DataFrame()
  for csv_file_path in csv_files_for_task_3:
    extracted_products_basic_info_data_frame = pd.concat(
      [
        extracted_products_basic_info_data_frame,
        pd.read_csv(csv_file_path)
      ],
      ignore_index = True
    )

  task_3_1_logger.info(f'Number of scraped product URLs: {extracted_products_basic_info_data_frame.shape[0]}')

  extracted_products_basic_info_data_frame = extracted_products_basic_info_data_frame[
    ~extracted_products_basic_info_data_frame.duplicated(subset = ['url'])
  ].reset_index(drop = True)

  task_3_1_logger.info(f'Number of unique product URLs: {extracted_products_basic_info_data_frame.shape[0]}')

  task_3_1_logger.info('Number of missing values per column:')
  task_3_1_logger.info(extracted_products_basic_info_data_frame.isna().sum())

  extracted_products_basic_info_data_frame.to_csv('data/unique_products_urls.csv', index = False)

  task_3_1_logger.info('Completed subtask')
