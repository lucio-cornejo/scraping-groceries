from src.instances import config, task_1_logger, driver

from src.categories_scraper import (
  click_show_all_categories_button_if_present,
  extract_categories_name_and_url 
)
from src.subcategories_scraper import (
  are_subcategories_available,
  save_list_as_JSON,
  flatten_list_of_categories_and_subcategories_url
)


if __name__ == '__main__':
  """
  Save into JSON file url of every Grocery category or subcategory
  """
  task_1_logger.info('Logging timestamps are respect to America/Lima timezone')

  # Access Groceries homepage
  driver.set_page_load_timeout(config['selenium']['page_load_seconds_timeout'])
  driver.get(config['groceries_homepage']['url'])

  # Show all categories
  try:
    click_show_all_categories_button_if_present()
  except Exception as e:
    task_1_logger.exception(e)

  categories_name_and_url = extract_categories_name_and_url()

  # Extract url of each subcategory, if found
  for category_dict in categories_name_and_url:
    category_url = category_dict['url']
    task_1_logger.info(f"Category: {category_dict['grocery_category']}")
    
    are_there_subcategories = are_subcategories_available(category_url)
    if not are_there_subcategories:
      task_1_logger.warning('No subcategories found')
      continue

    # Click button to show all categories, if available in website
    try:
      click_show_all_categories_button_if_present()
    except Exception as e:
      task_1_logger.exception(e)

    category_dict['subcategories'] = extract_categories_name_and_url()


  driver.quit()
  save_list_as_JSON(
    categories_name_and_url, 
    file_path = 'data/categories_and_subcategories_url.json'
  )

  """
  Create JSON list where each item contains an URL which points to a 
  website of multiple products, that will be used in the next task for
  scraping, page by page, the products' basic info 
  (title, main image url, (upc not yet), etc) .
  """
  url_dicts_list = flatten_list_of_categories_and_subcategories_url(
    categories_name_and_url
  )
  save_list_as_JSON(url_dicts_list, file_path = 'data/initial_urls_for_task_2.json')
