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

# %%
from src.get_non_deals_categories_url import (
  show_all_categories, extract_non_deals_categories_url
)

# %%
driver = get_chrome_driver(config['profile'])
driver.set_page_load_timeout(config['selenium']['page_load_seconds_timeout'])

# %%
driver.get(config['groceries_homepage']['url'])

# %%
show_all_categories.click_show_all_categories_button(
  driver, 
  categories_button_css_selector = ''.join([
    config['groceries_homepage']['categories_container']['css_selector'],
    config['groceries_homepage']['categories_container']['categories_button_appended_css_selector']
  ])
)

# %%
tmp = extract_non_deals_categories_url.extract_categories_name_and_url(
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
logger.info(tmp)