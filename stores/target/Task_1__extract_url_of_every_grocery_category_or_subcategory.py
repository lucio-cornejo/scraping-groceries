from dotenv import load_dotenv
load_dotenv()

from pyaml_env import parse_config
config = parse_config('config.yml', encoding = 'utf-8')


from src.setup_selenium_driver import get_chrome_driver
from src.categories_scraper import (
  click_show_all_categories_button_if_present,
  extract_categories_name_and_url 
)
from src.subcategories_scraper import (
  are_subcategories_available,
  save_list_of_urls_per_page_to_scrap
)

from src.logger import get_logger
logger = get_logger(
  config, 
  logs_file_name = 'grocery_cat_or_subcat_url_extraction.log'
)


if __name__ == '__main__':
  """
  Save into JSON file url of every Grocery category or subcategory
  """
  # Access Groceries homepage
  driver = get_chrome_driver(config)
  driver.set_page_load_timeout(config['selenium']['page_load_seconds_timeout'])
  driver.get(config['groceries_homepage']['url'])

  # Show all categories
  try:
    click_show_all_categories_button_if_present(config, driver)
  except Exception as e:
    logger.exception(e)

  categories_name_and_url = extract_categories_name_and_url(config, driver)

  # Extract url of each subcategory found
  for category_dict in categories_name_and_url:
    category_url = category_dict['url']
    logger.info(f"Category: {category_dict['grocery_category']}")
    
    are_there_subcategories = are_subcategories_available(config, driver, category_url)
    if not are_there_subcategories:
      logger.warning('No subcategories found')
      continue

    # Click button to show all categories, if available in website
    try:
      click_show_all_categories_button_if_present(config, driver)
    except Exception as e:
      logger.exception(e)

    category_dict['subcategories'] = extract_categories_name_and_url(config, driver)


  save_list_of_urls_per_page_to_scrap(
    categories_name_and_url, 
    file_path = './data/categories_and_subcategories_url.json'
  )
