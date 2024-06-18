from .instances import config

from tempfile import mkdtemp
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_chrome_driver() -> webdriver.Chrome:
  if config['profile'] == 'local':
    options = webdriver.ChromeOptions()
    options.add_argument("--guest")
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--disable-proxy-certificate-handler")
    # Avoid downloading images, to reduce page loading time
    options.add_argument('--blink-settings=imagesEnabled=false')
    # Do not wait for page load after accessing website
    # Source: https://stackoverflow.com/a/46339092
    options.page_load_strategy = 'eager'

    chrome_driver = webdriver.Chrome(
      service = Service(ChromeDriverManager().install()), 
      options = options
    )
    return chrome_driver

  if config['profile'] == 'production':
    options = webdriver.ChromeOptions()

    options.binary_location = '/opt/chrome/chrome'
    options.add_argument("--headless=new")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")

    chrome_driver = webdriver.Chrome(options = options)
    return chrome_driver
