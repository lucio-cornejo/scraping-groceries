from .instances import config

import requests  
from urllib.parse import urlparse
from requests_ip_rotator import ApiGateway  


def request_by_random_IPs(url: str) -> list[ApiGateway, requests.Session]:
  # AWS identification
  aws_region = config['aws']['region']
  aws_access_key_id = config['aws']['access_key_id']
  aws_access_key_secret = config['aws']['access_key_secret']

  # Set url and API name
  src = url
  src_parsed = urlparse(src)
  src_no_path = "%s://%s" % (src_parsed.scheme, src_parsed.netloc)

  # Initialize new API
  gateway = ApiGateway(src_no_path,
    regions = [aws_region],
    access_key_id = aws_access_key_id,
    access_key_secret = aws_access_key_secret
  )
  gateway.start()

  """
  From local tests of session get requests, 
  the IPs generated via 'session.<method(url, ...)>'
  will be different IF AND ONLY IF the url argument
  is the same as the url argument for this function .

  In the case of same url argument (both of them),
  there is no need to execute 'gateway.start()' more
  than once in order to use different IPs for session's methods
  """
  session = requests.Session()                       
  session.mount(src_no_path, gateway)

  # Do not forget to SHUTDOWN THE GATEWAY when done .
  # If not, AWS charges will increase .
  return (gateway, session)
