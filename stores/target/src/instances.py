# Parse config.yml
from dotenv import load_dotenv
from pyaml_env import parse_config
load_dotenv()
config = parse_config('config.yml', encoding = 'utf-8')


# Load loggers
from .logger import get_logger
task_1_1_logger = get_logger(logger_name = 'task_1.1')

task_2_1_logger = get_logger(logger_name = 'task_2.1')
task_2_2_logger = get_logger(logger_name = 'task_2.2')

task_3_1_logger = get_logger(logger_name = 'task_3.1')

task_4_1_logger = get_logger(logger_name = 'task_4.1')


# Load Selenium web driver
from .setup_selenium_driver import get_chrome_driver
driver = get_chrome_driver()
