# %%
from dotenv import load_dotenv
load_dotenv()

from pyaml_env import parse_config
config = parse_config('./config.yml', encoding = 'utf-8')
config

# %%
from src.logger import get_logger
from src.setup_selenium_driver import get_chrome_driver

# %%
