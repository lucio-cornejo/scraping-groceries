from bs4 import BeautifulSoup

import asyncio
import aiohttp
from codetiming import Timer

async def task(name, work_queue):
    timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            print(f"Task {name} getting URL: {url}")
            timer.start()
            async with session.get(url, ssl = False) as response:
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')

                # cats = soup.select('[data-test="@web/Breadcrumbs/BreadcrumbNav"] ol li')
                cats = soup.select('[data-test="@web/Breadcrumbs/BreadcrumbLink"]')
                category_tree = '/'.join(list(map(lambda level: level.text.strip(), cats)))
                print(category_tree)
      # .replace(/\s&amp;\s/g, ' & ');
                # soup.select('[data-test="@web/site-top-of-funnel/ProductDetailCollapsible-Specifications"]')
                # soup.select('[data-test="item-details-specifications"] > div')
                # soup.select('[data-test="@web/site-top-of-funnel/ProductDetailCollapsible-LabelInfo"]')



            timer.stop()

async def main():
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    work_queue = asyncio.Queue()

    # Put some work in the queue
    for url in [
        "https://www.target.com/p/kidfresh-frozen-chicken-meatballs-16-45oz/-/A-85356048#lnk=sametab",
        "https://www.target.com/p/oscar-mayer-jalapeno-cheddar-hot-dogs-16oz/-/A-91001109#lnk=sametab"
    ]:
        await work_queue.put(url)

    # Run the tasks
    with Timer(text="\nTotal elapsed time: {:.1f}"):
        await asyncio.gather(
          *[asyncio.create_task(task(f"Task {1 + index}", work_queue)) for index in range(len(url))]
        )


if __name__ == "__main__":
    asyncio.run(main())