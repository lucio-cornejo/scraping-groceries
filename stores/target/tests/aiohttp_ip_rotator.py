# python -m pip install aiohttp-ip-rotator==1.0
from src.instances import config, driver
driver.quit()

from src.subcategories_scraper import save_list_as_JSON

from asyncio import get_event_loop
from aiohttp_ip_rotator import RotatingClientSession

async def main():
  BASE_URL = "https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1"
  
  session = RotatingClientSession(
    # "https://api.ipify.org", 
    BASE_URL,
    config['aws']['access_key_id'],
    config['aws']['access_key_secret']
  )
  await session.start()

  
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
  

  for index in range(2):
    # response = await session.get("https://api.ipify.org")
    # print(f"Your ip: {await response.text()}")

    response = await session.get(
      BASE_URL,
      # Source: https://docs.aiohttp.org/en/stable/client_quickstart.html
      params = GET_request_params_list[index]
    )
    response_json = await response.json()

    print(response_json)
    # save_list_as_JSON(response_json, f'data/testing/{index}.json')

  await session.close()


if __name__ == "__main__":
  get_event_loop().run_until_complete(main())
