import sys
import logging.config
from yaml import safe_load

# Use Lima, Peru timezone for datetime in logs
# Source: https://stackoverflow.com/a/62265324
from pytz import timezone
from datetime import datetime
logging.Formatter.converter = lambda *args: datetime.now(tz = timezone('America/Lima')).timetuple()


def get_logger(config: dict, logger_name: str):
  if config['profile'] == 'local':
    # Configure the logging module via logging_config.yml
    # Source: https://medium.com/@cyberdud3/a-step-by-step-guide-to-configuring-python-logging-with-yaml-files-914baea5a0e5
    with open('logging_config.yml', 'rt') as f:
      logging_config = safe_load(f.read())
      
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(logger_name)
    return logger

  if config['profile'] == 'production':
    logger = logging.getLogger()
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
      logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
        "%Y/%m/%d %H:%M:%S %p"
      )
    )

    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    return logger
