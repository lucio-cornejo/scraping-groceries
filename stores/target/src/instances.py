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
task_3_2_logger = get_logger(logger_name = 'task_3.2')
task_3_3_logger = get_logger(logger_name = 'task_3.3')

task_4_2_logger = get_logger(logger_name = 'task_4.2')
