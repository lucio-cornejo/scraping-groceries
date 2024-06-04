# %%
URL = "https://www.target.com/p/applegate-naturals-family-size-chicken-nuggets-frozen-16oz/-/A-15389403"
# HEADERS = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36' }
HEADERS = {
  "authority" : "www.target.com",
  "User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
  "Accept " : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  "Accept-Encoding" : 'gzip, deflate, br, zstd',
  "Accept-Language" : 'en-US,en;q=0.9,es-US;q=0.8,es;q=0.7'
}

# %%
HEADERS = {
  "authority" : "www.target.com",
  "method" : "GET",
  "path" : "/p/applegate-naturals-family-size-chicken-nuggets-frozen-16oz/-/A-15389403",
  "scheme" : "https",
  "Accept " : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  "Accept-Encoding" : 'gzip, deflate, br, zstd',
  "Accept-Language" : 'en-US,en;q=0.9,es-US;q=0.8,es;q=0.7',
  "Cache-Control" : 'no-cache',
  # "Cookie" : 'visitorId=018EECDE90C702018E5EA8C77C7A126D; UserLocation=15000|-12.040|-77.020|LMA|PE; mdLogger=false; kampyle_userid=3eeb-7e02-9c29-c67b-aea7-1124-2e48-1ca7; fiatsCookie=DSI_671|DSN_Traverse%20City|DSZ_49684; sapphire=1; TealeafAkaSid=ct7siYWUhArzA_ZB62eqz5M9qvpqj0V0; crl8.fpcuid=5bf79557-951e-4e5f-acff-c857684091b6; GuestLocation=15000|-12.040|-77.020|LMA|PE; ffsession={%22sessionHash%22:%224328ee247145e1717293099193%22}; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIwYzliMTUzMS0xOTk2LTQ0OTAtYmFmYi0zNTE2NjNkYjZmZmYiLCJpc3MiOiJNSTYiLCJleHAiOjE3MTczNzk1MDAsImlhdCI6MTcxNzI5MzEwMCwianRpIjoiVEdULjMyOGU2NzIwNDY3MzQ1NDM5ZTFiYmE5YTI3ZDQ3MGY3LWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6IjZkODljODQ5MmUyZDFlYTFhMTYyZjgwMzYwMGFlMWRjMDQ5N2I4YTVkYjNjYzJhZjc5ZDIwMTc0MDNiYzE4YTMiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.gs0mxFi6mcT6Wt_a3yVKkZiPrMa9W2Gk6iwoOCbgdq5eqagCdw2FF2LF-0njjP0A3CL6fN9El0heg5nlGEzLUYnpZGRQx35t-G4Ny1AyjSDRjkxk7AZnKfOQWRiamA24Hyv1MAx_ROiohlc0BHSNwpaPkKIXwHL5FHKUYW4MKcEREgya7rCpAj3KGVNFiiJHCkfDdvW5ODNPwe3FU3RZ0Hm4XDzjIJC7x_3i9bHEZ6chdEzfjzcxnFqKjbVt6Co9BMnVVJl5G6mUnyAqYPV359kEnEnI2qN-6eyC3s7uNKLoIqKWLqaqghhSqtyDhfEsovfsU48ohQPkyO4jkyYuzw; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiIwYzliMTUzMS0xOTk2LTQ0OTAtYmFmYi0zNTE2NjNkYjZmZmYiLCJpc3MiOiJNSTYiLCJleHAiOjE3MTczNzk1MDAsImlhdCI6MTcxNzI5MzEwMCwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlLCJzdCI6IkxNQSJ9fQ.; refreshToken=7Ot57B-bwfF1JdyR0LEcS6HZ1qGOoD2xIsiybAwQYdTKOGn6JDByO-ST5hq9wucmZfrAlWO8nRx4ForMPoEJWQ; __gads=ID=e029f77990374f0b:T=1716663637:RT=1717298337:S=ALNI_MZaS62o7VszAu5WqR0E4ZZ-cEcKmA; __gpi=UID=00000e2d833166e7:T=1716663637:RT=1717298337:S=ALNI_MZvi9YD-lTVvGW9kbeRUdo0FtbSRg; __eoi=ID=63adcdda94599c84:T=1716663637:RT=1717298337:S=AA-AfjakFQzgwrFeYZS_MSpgXbR4; dteRfWys=1trrlclz; kampyleUserSession=1717298453852; kampyleUserSessionsCount=51; kampyleSessionPageCounter=1',
  "Pragma" : 'no-cache',
  "Priority" : 'u=0, i',
  "Sec-Ch-Ua" : '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
  "Sec-Ch-Ua-Mobile" : '?0',
  "Sec-Ch-Ua-Platform" : '"Windows"',
  "Sec-Fetch-Dest" : 'document',
  "Sec-Fetch-Mode" : 'navigate',
  "Sec-Fetch-Site" : 'same-origin',
  "Sec-Fetch-User" : '?1',
  "Upgrade-Insecure-Requests" : '1',
  "User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}


# %%
import requests

res = requests.get(URL, headers = HEADERS)
res.text

# %%
from bs4 import BeautifulSoup
import json

soup = BeautifulSoup(res.text, 'html.parser')
soup

# %%
nutritional_info = soup.find('[data-test="productDetailTabs-nutritionFactsTab"] .h-padding-h-default')
print(nutritional_info)

# %%


# %%

nutrition_info_json = {}

# Extract serving size and servings per container
nutrition_info_json['Serving Size'] = soup.find(string = "Serving Size: ").find_next().text
nutrition_info_json['Servings Per Container'] = soup.find(string = "Serving Per Container: ").find_next().text

# Extract calories
nutrition_info_json['Calories'] = soup.find(string = "Calories: ").find_next().text

# Extract nutrient details
daily_values = soup.find(class_="styles__DailyValues-sc-17y8f4z-6")

nutrients = daily_values.find_all("div", class_="h-margin-t-tight")

# %%
nutrients[0].find_all('span')

# %%
for nutrient in nutrients:
    name = nutrient.find("b").text
    value = nutrient.find_all("span")[1].previous_sibling.strip()
    daily_value = nutrient.find("span", class_="h-float-right").text if nutrient.find("span", class_="h-float-right") else None
    nutrition_info_json[name] = {"Value": value, "Daily Value": daily_value}

# Save to JSON file
with open('nutrition_info.json', 'w') as f:
    json.dump(nutrition_info_json, f, indent = 2)

print('Nutritional information has been saved to nutrition_info.json')
