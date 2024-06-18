# Scraping **Target**

## Tasks

For this project, all commands for executing Python scripts
are supossed to be used after having activated the virtual environment,
and with `stores/target` as root folder .

### Task 1

#### Subtask 1.1

- **File**: `tasks/task_1/grocery_categories_and_subcategories_url_extraction.py`

- **Goal**: Extract URLs of categories or subcategories which are expected
to direct to a **paginated** website displaying multiple products.

- **Command for execution**: `python -m tasks.task_1.grocery_categories_and_subcategories_url_extraction`

- **Execution time**: 4 minutes


#### Subtask 1.2

- **File**: `tasks/task_1/paginated_products_webpage_filter.js`

- **Goal**: Filter which URLs extracted in task-1.1 point to a **paginated** products website,
based on the HTML content of such websites.

- **Command for execution**: `node ./tasks/task_1/paginated_products_webpage_filter.js`

- **Execution time**: 0.5 minutes


### Task 2

#### Subtask 2.1

- **File**: `tasks/task_2/products_basic_info_get_request_url_extraction.py`

- **Goal**: Visit every URL in file `urls_for_task_2.1.json` to extract
which **GET request** gets executed in order to fetch the products' basic information,
products corresponding to the URL's grocery **group** (category or subcategory with paginated products website).

- **Command for execution**: `python -m tasks.task_2.products_basic_info_get_request_url_extraction`

- **Execution time**: 16 minutes


#### Subtask 2.2




- **Goal**: Extract the URLs of the websites (sometimes is a grocery subcategory,
but other times it's just a grocery category) which display multiple products
- **File**: `tasks/grocery_categories_and_subcategories_url_extraction.py`
- **Command for task execution**: Inside `target` directory, activate the 
Python virtual environment and then execute `python -m tasks.grocery_categories_and_subcategories_url_extraction` .


### Task 2

- **Status**: Completed code, but pending execution and optimization .

- **Goal**: For each grocery product, extract its main-image url, 
title, `tcin` value, `store-id`, and other parameters required for the next main 
task. However, `upc` and label info  extraction does not seem possible at this stage,
but for the next main task .

- **File**: `tasks/grocery_products_basic_info_extraction.py`

- **Command for task execution**: Inside `target` directory, activate the 
Python virtual environment and then execute `python -m tasks.grocery_products_basic_info_extraction` .


**Pending** to use Python's seleniumwire package to intercept the get request response
where the products' basic info is present (no need to extract it from website).

Example: <https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&category=5xsz2&channel=WEB&count=24&default_purchasability_filter=true&include_dmc_dmr=true&include_sponsored=true&new_search=false&offset=24&page=%2Fc%2F5xsz2&platform=desktop&pricing_store_id=671&spellcheck=true&store_ids=671%2C1246%2C924&useragent=Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F125.0.0.0+Safari%2F537.36&visitor_id=018EECDE90C702018E5EA8C77C7A126D&zip=15000>


### Task 3

- **Status**: Pending code, due to Target temporary (half a day) IP ban.

- **Goal**: For each grocery product, extract it's label info and UPC.

- **File**: `tasks/grocery_products_info_download.js`

- **Command for task execution**: Inside `target` directory, 
execute `node ./tasks/grocery_products_last_info_download.js`


- Useful Target links
  - **Extract product's UPC**: 
      - Example: <https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&tcin=88333669&pricing_store_id=1>
      - Only the `tcin` parameter's value seems to be necessary to change in order for the UPC extraction to work for multiple products.
      - For the products' url, as in the file `data/products_urls.json`, the `tcin` parameter's value corresponds to, for example:
          - Product url: **https://www.target.com/p/van-zyverden-12-34-pineapple-lily-with-stainless-metal-planter-soil-and-growers-pot-eucomis/-/A-91835796#lnk=sametab**
          - Product's `tcin` value: "91835796"


## Python packages installed

```
python-dotenv==1.0.1
pyaml-env==1.2.1
pytz==2024.1
selenium==4.19.0
webdriver-manager==4.0.1
selenium-wire==5.1.0
blinker==1.7.0
pandas==2.0.1
requests-ip-rotator==1.0.14
```
