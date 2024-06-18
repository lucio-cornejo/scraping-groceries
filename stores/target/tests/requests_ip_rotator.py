# %%
import os; os.chdir('./../')

# %%
from src.ip_rotator import create_gateway_and_session_for_random_IP

# %%
BASE_URL = "https://redsky.target.com"
ENDPOINT_URL = "https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1"
HEADERS = { 
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}


GET_request_params_list = [
  {
    "key" : "9f36aeafbe60771e321a7cc95a78140772ab3e96",
    "tcin" : "47868632",
    "pricing_store_id" : "3991",
    "visitor_id" : "018EECDE90C702018E5EA8C77C7A746.49747804478D",
    "channel" : "WEB",
    "page" : "%2Fp%2FA-47868632"
  },
  {
    "key" : "9f36aeafbe60771e321a7cc95a78140772ab3e96",
    "tcin" : "13234505",
    "pricing_store_id" : "3991",
    "visitor_id" : "018EECDE90C702018E5EA8C77C7A506.15976511843434D",
    "channel" : "WEB",
    "page" : "%2Fp%2FA-13234505"
  }
]

GET_REQUEST_URL = ENDPOINT_URL + '?' + '&'.join(
  [
    f'{key}={value}' 
    for key, value in GET_request_params_list[0].items()
  ]
)
GET_REQUEST_URL

# %%
gateway, session = create_gateway_and_session_for_random_IP(GET_REQUEST_URL)

rsp = session.get(GET_REQUEST_URL, headers = HEADERS)
rsp.json()

# %%
gateway.shutdown()

# %%
gateway, session = create_gateway_and_session_for_random_IP(ENDPOINT_URL)

rsp = session.get(
  ENDPOINT_URL, 
  headers = HEADERS, 
  params = GET_request_params_list[0]
)

# %%
rsp.json()

# %%
gateway.shutdown()
