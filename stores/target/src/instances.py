# Parse config.yml
from dotenv import load_dotenv
load_dotenv()

from pyaml_env import parse_config
config = parse_config('config.yml', encoding = 'utf-8')

# Load logger
from src.logger import get_logger
task_one_logger = get_logger(config, logs_file_name = 'grocery_cat_or_subcat_url_extraction.log')
task_two_logger = get_logger(config, logs_file_name = 'grocery_products_url_extraction.log')

# Load Selenium web driver
from src.setup_selenium_driver import get_chrome_driver
driver = get_chrome_driver(config)
