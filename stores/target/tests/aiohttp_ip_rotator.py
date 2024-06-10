# python -m pip install aiohttp-ip-rotator==1.0
from src.instances import config, driver
driver.quit()

from asyncio import get_event_loop
from aiohttp_ip_rotator import RotatingClientSession

async def main():
  session = RotatingClientSession(
    "https://api.ipify.org", 
    config['aws']['access_key_id'],
    config['aws']['access_key_secret']
  )
  await session.start()
  for _ in range(20):
    response = await session.get("https://api.ipify.org")
    print(f"Your ip: {await response.text()}")
  await session.close()


if __name__ == "__main__":
  get_event_loop().run_until_complete(main())
