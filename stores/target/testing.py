# %%
from src.instances import config, driver

import json
import gzip

# Create list where each element contains an url for Selenium,
# from which's website the products' basic info will be extracted
with open('data/urls_for_task_2.json', 'r', encoding = 'utf-8') as f:
  urls_multiple_products_pages = json.loads(f.read())

PRODUCTS_BASIC_INFO_PATTERN_URL ="https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2"


def filter_products_basic_info_get_request(url_index: int):
  del driver.requests
  driver.get(urls_multiple_products_pages[url_index]['url'])
  driver.wait_for_request(PRODUCTS_BASIC_INFO_PATTERN_URL, timeout = 60)

  products_basic_info_get_request = list(filter(
    lambda request: PRODUCTS_BASIC_INFO_PATTERN_URL in request.url,
    driver.requests
  ))
  if len(products_basic_info_get_request) > 1:
    raise Exception("More than one request matched the url pattern")

  # Decode gzip encoded data (source: https://stackoverflow.com/a/6731319)
  response_json = json.loads(
    str(gzip.decompress(products_basic_info_get_request[0].response.body), 'utf-8')
  )
  response_json

  return (products_basic_info_get_request[0], response_json['data']['search'])


# %%
result = filter_products_basic_info_get_request(0)
# result = filter_products_basic_info_get_request(-1)
result

# %%
result[0].url

# %%
list(map(
  lambda e: e['item']['product_description']['title'],
  result[1]['products']
))

# %%
HEADERS = dict(zip(
  [x[0] for x in list(result[0].headers.raw_items())],
  [x[1] for x in list(result[0].headers.raw_items())]
))
HEADERS

# %%
import requests

response = requests.get(result[0].url, headers = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
})
response

# %%
response.json()

# %%
"https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2?" + '&'.join([
  "key=9f36aeafbe60771e321a7cc95a78140772ab3e96",
  "category=wdysv",
  "channel=WEB",
  "count=28",
  # "count=24",
  "default_purchasability_filter=true",
  "include_dmc_dmr=true",
  "include_sponsored=true",
  "new_search=false",
  # "offset=0",
  "offset=1199",
  "page=%2Fc%2Fwdysv",
  "platform=desktop",
  "pricing_store_id=2768",
  "spellcheck=true",
  "store_ids=2768%2C2766%2C3264%2C3353%2C3240",
  "useragent=Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F125.0.0.0+Safari%2F537.36",
  "visitor_id=1",
  # "visitor_id=018FF39DD08D0201BA59572B9BAE3DF2",
  "zip=15400"
])


# o['data']['search']['products'].map(e => e?.item?.product_description?.title)
# %%
"""
https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2?
  key=9f36aeafbe60771e321a7cc95a78140772ab3e96 
  category=54wac
  channel=WEB
  count=24
  default_purchasability_filter=true
  include_dmc_dmr=true
  include_sponsored=true
  new_search=false
  offset=0
  page=%2Fc%2F54wac
  platform=desktop
  pricing_store_id=2768
  spellcheck=true
  store_ids=2768%2C2766%2C3264%2C3353%2C3240
  useragent=Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F125.0.0.0+Safari%2F537.36
  visitor_id=018FF3DCD27B0201A01F4EFA14888102
  zip=15400
"""


# %%
import requests

response = requests.get(
  "https://www.target.com/c/frozen-single-serve-meals-foods-grocery/-/N-wdysv",
  headers =  {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
  }
)
response

# %%
print(response.text)

# %%
'11' in 
# %%
print(response.text.split('11')[2])

# %%
redsky = list(filter(
  lambda e: 'redsky' in e.url,
  driver.requests
))
redsky

# %%
json.loads(str(gzip.decompress(redsky[3].response.body), 'utf-8'))

# %%
str(gzip.decompress(redsky[3].response.body), 'utf-8').split('ockets')[0]

# %%
# %%
# %%
import requests  
from urllib.parse import urlparse
from requests_ip_rotator import ApiGateway  

# requests==2.27.1
# urllib is a Python3 standard library
# requests-ip-rotator==1.0.14

# %%
def request_by_random_IPs(url):
  # AWS identification
  aws_region = ''
  aws_access_key_id = ''
  aws_access_key_secret = ''

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
  return { "gateway" : gateway, "session" : session }

# %%
"""
url = 'https://wb2server.congreso.gob.pe/spley-portal-service/dictamen/lista-con-filtro'
tmp = request_by_random_IPs(url)
data = {
  "perParId": None, 
  "perLegId": None,
  "comisionId": None, 
  "texto": None
}

x = tmp["session"].post(url, json = data)
tmp["gateway"].shutdown()
x
"""

# %%
"""
HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}
url_dictamenes = 'https://wb2server.congreso.gob.pe/spley-portal-service/dictamen/lista-con-filtro'

tmp = request_by_random_IPs(url_dictamenes)
response = tmp["session"].head(url_dictamenes, headers = HEADERS)
tmp["gateway"].shutdown()

response
"""

# %%
"""
Basic examples of user IP retrieval
"""
# src = 'https://checkip.amazonaws.com'
# src_parsed = urlparse(src)
# src_nopath = "%s://%s" % (src_parsed.scheme, src_parsed.netloc)

# rsp = requests.get(src_nopath)
# rsp.text.strip()

# %%
url = 'https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&category=wdysv&channel=WEB&count=28&default_purchasability_filter=true&include_dmc_dmr=true&include_sponsored=true&new_search=false&offset=1199&page=%2Fc%2Fwdysv&platform=desktop&pricing_store_id=2768&spellcheck=true&store_ids=2768%2C2766%2C3264%2C3353%2C3240&useragent=Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F125.0.0.0+Safari%2F537.36&visitor_id=1&zip=15400'
api = request_by_random_IPs(url)
gateway = api["gateway"]
session = api["session"]

# %%
# rsp = session.get('https://www.google.com/')
# rsp = session.get('https://api.ipify.org/')
# rsp = session.get(url)
# rsp, rsp.text.strip()

# %%
rsp = session.get(url)
rsp

# %%
json.loads(rsp.text)['data']['search']['search_response']['metadata']
gateway.shutdown()
