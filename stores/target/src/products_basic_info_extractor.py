# %%
import os; os.chdir('./../')

# %%
import re

def extract_category_code_from_products_url(products_url: str) -> str:
  """
  @param products_url: Example: "https://www.target.com/c/frozen-single-serve-meals-foods-grocery/-/N-wdysv"
  @return: The example's output would be "wdysv"
  """
  url_text_before_category = "/-/N-"
  return re.search(rf'(?<={url_text_before_category}).*', products_url).group(0).strip()


# %%
def assemble_url_for_products_page_get_request(
  category_code: str, number_of_products: int, items_offset: int, visitor_id: str
) -> str:
  return ''.join([
    "https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2?",
    # Query string parameters
    '&'.join([
      "key=9f36aeafbe60771e321a7cc95a78140772ab3e96",
      f"category={category_code}",  # "category=wdysv",
      "channel=WEB",
      f"count={number_of_products}",  # "count=24",
      "default_purchasability_filter=true",
      "include_dmc_dmr=true",
      "include_sponsored=true",
      "new_search=false",
      f"offset={items_offset}",  # "offset=0",
      f"page=%2Fc%2F{category_code}",  # "page=%2Fc%2Fwdysv",
      "platform=desktop",
      "pricing_store_id=2768", #######
      "spellcheck=true",
      "store_ids=",  ######
      # "store_ids=2768%2C2766%2C3264%2C3353%2C3240",  ######
      "useragent=Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F125.0.0.0+Safari%2F537.36",
      f"visitor_id={visitor_id}",  # "visitor_id=018FF39DD08D0201BA59572B9BAE3DF2",
      "zip=15400"
    ])
  ])


# %%
import json

with open('data/initial_urls_for_task_2.json', 'r', encoding = 'utf-8') as f:
  urls = json.loads(f.read())

urls

# %%
subcat = list(filter(
  lambda d: 'grocery_subcategory' in d.keys(),
  urls
))
subcat

# %%
cat_code = extract_category_code_from_products_url(subcat[0]['url'])
cat_code

# %%