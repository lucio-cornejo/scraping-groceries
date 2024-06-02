# Parse config.yml
from dotenv import load_dotenv
load_dotenv()

from pyaml_env import parse_config
config = parse_config('config.yml', encoding = 'utf-8')


# Load loggers
from .logger import get_logger
task_one_logger = get_logger(logger_name = 'task_one')
task_two_logger = get_logger(logger_name = 'task_two')


# Load Selenium web driver
from .setup_selenium_driver import get_chrome_driver
driver = get_chrome_driver()
