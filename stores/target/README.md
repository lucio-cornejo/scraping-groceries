# Scraping **Target**

## Tasks

For this project, all commands for executing Python scripts
are supossed to be used after having activated the virtual environment,
and with `stores/target` as root folder .

### Task 1

#### Subtask 1.1

- **File**: `tasks/task_1/task_1_1/grocery_categories_and_subcategories_url_extraction.py`

- **Goal**: Extract URLs of categories or subcategories which are expected
to direct to a **paginated** website displaying multiple products.

- **Command for execution**: `python -m tasks.task_1.task_1_1.grocery_categories_and_subcategories_url_extraction`

- **Execution time**: 4 minutes


#### Subtask 1.2

- **File**: `tasks/task_1/task_1_2/paginated_products_webpage_filter.js`

- **Goal**: Filter which URLs extracted in task-1.1 point to a **paginated** products website,
based on the HTML content of such websites.

- **Command for execution**: `node ./tasks/task_1/task_1_2/paginated_products_webpage_filter.js`

- **Execution time**: 0.5 minutes


### Task 2

#### Subtask 2.1

- **File**: `tasks/task_2/task_2_1/products_basic_info_get_request_url_extraction.py`

- **Goal**: Visit every URL in file `urls_for_task_2.1.json` to extract
which **GET request** gets executed in order to fetch the products' basic information,
products corresponding to the URL's grocery **group** (category or subcategory with paginated products website).

- **Command for execution**: `python -m tasks.task_2.task_2_1.products_basic_info_get_request_url_extraction`

- **Execution time**: 16 minutes


#### Subtask 2.2

- Requires **Amazon Web Services** account, due to API Gateway use.

- **File**: `tasks/task_2/task_2_2/grocery_products_basic_info_extraction.py`

- **Goal**: Extract every grocery product's basic info (tcin,original_tcin,dpci,title,url,image_url,merged_bread_crumbs), by appropriately modifying each group product's GET request url contained
in file `data/get_request_urls_for_task_2.2.json` .

- **Command for execution**: `python -m tasks.task_2.task_2_2.grocery_products_basic_info_extraction`

- **Execution time**: 11 minutes


### Task 3

#### Task 3.1


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
