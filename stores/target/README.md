# Scraping **Target**

## Tasks

1. `tasks/grocery_categories_and_subcategories_url_extraction.py`
1. `tasks/grocery_products_url_extraction.py`


## Useful Target links

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
```
