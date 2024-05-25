# %%
from dotenv import load_dotenv
load_dotenv()

from pyaml_env import parse_config
config = parse_config('./config.yml', encoding = 'utf-8')


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from src.logger import get_logger
from src.setup_selenium_driver import get_chrome_driver

from src.filter_non_deal_categories import filter_non_deal_categories

# %%
driver = get_chrome_driver(config['profile'])
driver.set_page_load_timeout(config['selenium']['page_load_seconds_timeout'])

# %%
driver.get(config['groceries_homepage']['url'])

# %%
WebDriverWait(driver, 10).until(
  EC.element_to_be_clickable((
    By.CSS_SELECTOR, 
    ''.join([
      config['groceries_homepage']['categories_container']['css_selector'],
      config['groceries_homepage']['categories_container']['categories_button_appended_css_selector']
    ])
  ))
).click()

# %%
categories_elements = driver.find_elements(
  By.CSS_SELECTOR, 
  ''.join([
    config['groceries_homepage']['categories_container']['css_selector'],
    config['groceries_homepage']['categories_container']['categories_element_appended_css_selector']
  ])
)
len(categories_elements)

# %%
categories_name_container_css_selector = ''.join([
  config['groceries_homepage']['categories_container']['css_selector'],
  config['groceries_homepage']['categories_container']['categories_name_container_appended_css_selector']
])

groceries_categories = filter_non_deal_categories(categories_elements, categories_name_container_css_selector)
len(groceries_categories)
