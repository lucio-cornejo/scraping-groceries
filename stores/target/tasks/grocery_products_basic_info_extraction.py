from src.instances import config, task_two_logger, driver
driver.quit()

from src.setup_selenium_driver import get_chrome_driver

from src.products_scraper import (
  parse_number_of_pages_from_web_text,
  load_all_products_in_page,
  is_products_website_paginated,
  extract_products_url_and_image_url,
  click_next_page_in_products_website
)

import asyncio
import json
from time import sleep
from codetiming import Timer

# Create list where each element contains an url for Selenium,
# from which's website the products' basic info will be extracted
with open('data/categories_and_subcategories_url.json', 'r', encoding = 'utf-8') as f:
  selenium_url_dicts_list = json.loads(f.read())



max_number_of_concurrent_tasks = 3
sem = asyncio.Semaphore(max_number_of_concurrent_tasks)


async def download_products_pages_titles_and_urls(work_queue):
  while not work_queue.empty():
    url_dict = await work_queue.get()
    task_two_logger.info(f"Started task for url: {url_dict['url']}")

    driver = get_chrome_driver()
    driver.get(url_dict['url'])
    sleep(10)




async def safe_download(work_queue):
  async with sem:  # semaphore limits num of simultaneous downloads
    return await download_products_pages_titles_and_urls(work_queue)


async def main():
  # tasks = [
  #   asyncio.ensure_future(safe_download(products_page_dict))  # creating task starts coroutine
  #   for products_page_dict in selenium_url_dicts_list[-3:]
  # ]
  # # Await moment all downloads are completed
  # await asyncio.gather(*tasks)  

  work_queue = asyncio.Queue()                                                                                                                                                                                                                                                              

  # Put some work in the queue
  for url_dict in selenium_url_dicts_list:
    await work_queue.put(url_dict)

  with Timer(text="\nTotal elapsed time: {:.1f}"):
    await asyncio.gather(
      *[asyncio.create_task(safe_download(work_queue)) for _ in range(len(selenium_url_dicts_list))]
    )

if __name__ == "__main__":
    asyncio.run(main())


# if __name__ ==  '__main__':
#     loop = asyncio.get_event_loop()
#     try:
#         loop.run_until_complete(main())
#     finally:
#         loop.run_until_complete(loop.shutdown_asyncgens())
#         loop.close()



# if __name__ == '__main__':
#   """
#   Save into JSON file url, image url, grocery category 
#   and grocery subcategory of every grocery product
#   """
#   task_two_logger.info('Logging timestamps are respect to America/Lima timezone')



#   driver.set_page_load_timeout(config['selenium']['page_load_seconds_timeout'])

#   products_basic_info = []
#   for category_dict in categories_and_subcategories_url_list:
#     grocery_category = category_dict['grocery_category']
    
    
#     if grocery_category != "Fresh Flowers":
#       continue


#     task_two_logger.info(f'Grocery category: {grocery_category}')

#     if not 'subcategories' in category_dict.keys():
#       task_two_logger.info('No subcategories available')
#       driver.get(category_dict['url'])
#       load_all_products_in_page()

#       number_of_products_pages = 1
#       is_website_paginated =  is_products_website_paginated()

#       if is_website_paginated:
#         number_of_products_pages = parse_number_of_pages_from_web_text()

#       task_two_logger.info(f'Number of products pages: {number_of_products_pages}')

#       # Extract each product url and its image url, per products page
#       for page_number in range(number_of_products_pages):
#         task_two_logger.info(f'Page number: {1 + page_number}')

#         if page_number > 0: load_all_products_in_page()

#         products_basic_info += extract_products_url_and_image_url(
#           grocery_category = grocery_category, grocery_subcategory = None
#         )

#         if is_website_paginated: click_next_page_in_products_website()
    
#     else:
#       for subcategory_dict in category_dict['subcategories']:
#         subcategory_name = subcategory_dict["grocery_category"]
#         task_two_logger.info(f'Subcategory: {subcategory_name}')
#         driver.get(subcategory_dict['url'])
#         load_all_products_in_page()

#         number_of_products_pages = 1
#         is_website_paginated =  is_products_website_paginated()

#         if is_website_paginated:
#           number_of_products_pages = parse_number_of_pages_from_web_text()

#         task_two_logger.info(f'Number of products pages: {number_of_products_pages}')

#         # Extract each product url and its image url, per products page
#         for page_number in range(number_of_products_pages):
#           task_two_logger.info(f'Page number: {1 + page_number}')

#           if page_number > 0: load_all_products_in_page()

#           products_basic_info += extract_products_url_and_image_url(
#             grocery_category = grocery_category, 
#             grocery_subcategory = f"'{subcategory_name}'"
#           )

#           if is_website_paginated: click_next_page_in_products_website()


#   driver.quit()
#   with open('data/products_urls.json', 'w', encoding = 'utf-8') as f:
#     json.dump(products_basic_info, f, indent = 4)
