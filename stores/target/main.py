# %%
from dotenv import load_dotenv
load_dotenv()

from pyaml_env import parse_config
config = parse_config('./config.yml', encoding = 'utf-8')

# %%
from src.logger import get_logger
logger = get_logger(config['profile'])

# %%
from src.setup_selenium_driver import get_chrome_driver

from src.get_non_deals_categories_url import (
  show_all_categories, extract_non_deals_categories_url
)

from src.get_non_deals_subcategories_url import are_subcategories_available

from src.get_products_url import (
  extract_number_of_pages
)

# %%
driver = get_chrome_driver(config['profile'])
driver.set_page_load_timeout(config['selenium']['page_load_seconds_timeout'])

# %%
driver.get(config['groceries_homepage']['url'])

# %%
# Click button to show all categories, if available in website
try:
  show_all_categories.click_show_all_categories_button_if_present(
    driver, 
    categories_button_css_selector = ''.join([
      config['groceries_homepage']['categories_container']['css_selector'],
      config['groceries_homepage']['categories_container']['categories_button_appended_css_selector']
    ])
  )
except Exception as e:
  logger.exception(e)

# %%
categories_name_and_url = extract_non_deals_categories_url.extract_categories_name_and_url(
  driver, 
  categories_element_css_selector = ''.join([
    config['groceries_homepage']['categories_container']['css_selector'],
    config['groceries_homepage']['categories_container']['categories_element_appended_css_selector']
  ]),
  categories_name_container_css_selector = ''.join([
    config['groceries_homepage']['categories_container']['css_selector'],
    config['groceries_homepage']['categories_container']['categories_name_container_appended_css_selector']
  ])
)
categories_name_and_url

# %%
for category_dict in categories_name_and_url:
  category_url = category_dict['url']

  are_there_subcategories = are_subcategories_available.are_subcategories_available(
    driver, category_url, config['groceries_homepage']['categories_container']['css_selector']
  )
  if not are_there_subcategories:
    continue

  # Click button to show all categories, if available in website
  try:
    show_all_categories.click_show_all_categories_button_if_present(
      driver, 
      categories_button_css_selector = ''.join([
        config['groceries_homepage']['categories_container']['css_selector'],
        config['groceries_homepage']['categories_container']['categories_button_appended_css_selector']
      ])
    )
  except Exception as e:
    logger.exception(e)

  category_dict['subcategories'] = extract_non_deals_categories_url.extract_categories_name_and_url(
    driver, 
    categories_element_css_selector = ''.join([
      config['groceries_homepage']['categories_container']['css_selector'],
      config['groceries_homepage']['categories_container']['categories_element_appended_css_selector']
    ]),
    categories_name_container_css_selector = ''.join([
      config['groceries_homepage']['categories_container']['css_selector'],
      config['groceries_homepage']['categories_container']['categories_name_container_appended_css_selector']
    ])
  )

# %%
categories_name_and_url[0]['subcategories']

# %%
products_website_number_of_pages = extract_number_of_pages.try_parsing_number_of_pages_from_web_text(
  driver, 
  number_of_pages_element_css_selector = ''.join([
    config['products_website']['paginator']['css_selector'],
    config['products_website']['paginator']['number_of_pages_element_appended_css_selector']
  ])
)
products_website_number_of_pages
