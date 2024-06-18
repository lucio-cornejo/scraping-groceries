from src.instances import config, task_1_1_logger
from src.web_driver_instance import driver

from src.categories_scraper import (
  click_show_all_categories_button_if_present,
  extract_categories_name_and_url 
)
from src.subcategories_scraper import (
  are_subcategories_available,
  save_list_as_JSON,
  flatten_list_of_categories_and_subcategories_url
)


def extract_urls_of_categories_and_subcategories():
  # Access Groceries homepage
  driver.set_page_load_timeout(config['selenium']['page_load_seconds_timeout'])
  driver.get(config['groceries_homepage']['url'])
  click_show_all_categories_button_if_present()

  categories_name_and_url = extract_categories_name_and_url()

  # Extract url of each subcategory, if found
  for category_dict in categories_name_and_url:
    category_url = category_dict['url']
    task_1_1_logger.info(f"Category: {category_dict['grocery_category']}")
    
    are_there_subcategories = are_subcategories_available(category_url)
    if not are_there_subcategories:
      task_1_1_logger.info('No subcategories found')
      continue

    # Click button to show all categories, if available in website
    try:
      click_show_all_categories_button_if_present()
    except:
      task_1_1_logger.info('All subcategories are shown by default in website')

    category_dict['subcategories'] = extract_categories_name_and_url(
      is_subcategories_extraction = True, 
      category_name_for_subcategories = category_dict['grocery_category']
    )


  driver.quit()
  save_list_as_JSON(
    categories_name_and_url, 
    file_path = 'data/categories_and_subcategories_url.json'
  )

  """
  Create list where each item contains a group (category or subcategory)
  URL corresponding to a possibly paginated website of products
  """
  url_dicts_list = flatten_list_of_categories_and_subcategories_url(
    categories_name_and_url
  )
  save_list_as_JSON(url_dicts_list, file_path = 'data/urls_for_task_1.2.json')


if __name__ == '__main__':
  try:
    task_1_1_logger.info('Started subtask')
    extract_urls_of_categories_and_subcategories()
    task_1_1_logger.info('Completed subtask')
  except Exception as e:
    task_1_1_logger.exception(e)
