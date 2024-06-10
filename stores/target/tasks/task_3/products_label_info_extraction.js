const fs = require("fs"); 
const Math = require('mathjs');
const async = require("async");

const productsObjectsArray = JSON.parse(fs.readFileSync('data/unique_products_urls.json', 'utf8'));
productsObjectsArray.splice(2);

async function fetchProductInfo(index) {
  const tcinOfProduct = productsObjectsArray[index]['tcin'].toString();
  console.log(tcinOfProduct);

  const randomThreeDigitInteger = Math.random(100, 999);

  const GETRequesURL = 'https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?' + 
    [
      'key=9f36aeafbe60771e321a7cc95a78140772ab3e96',
      `tcin=${tcinOfProduct}`,
      // 'is_bot=false',  // this does not seem necessary, but maybe it's useful
      // 'store_id=671', 
      'pricing_store_id=3991', // Does not seem to require value change per product
      // 'has_pricing_store_id=true', 
      // 'has_financing_options=true', 
      // 'include_obsolete=true', 
      `visitor_id=018EECDE90C702018E5EA8C77C7A${randomThreeDigitInteger}D`, 
      // 'has_size_context=true', 
      // 'skip_personalized=true', 
      // 'skip_variation_hierarchy=true', 
      'channel=WEB', 
      `page=%2Fp%2FA-${tcinOfProduct}`
    ].reduce((a, b) => a + '&' + b);
  
  console.log(GETRequesURL);
  const response = await fetch(GETRequesURL);
  console.log(response.status)

  if (response.status == 200) {
    const productJSON = await response.json();

    let productItem;
    if (productJSON['data']['product'].hasOwnProperty('children')) {
      if (productJSON['data']['product']['children'].some(productItem => productItem?.tcin === tcinOfProduct)) {
        productItem = productJSON['data']['product']['children']
          .filter(productItem => productItem?.tcin === tcinOfProduct)
          [0]
          ['item'];      
      } else {
        throw new Error('Failed extracttion of product children with matching tcin value')
      }
    } else {
      productItem = productJSON['data']['product']['item'];
    }

    productsObjectsArray[index]['nutrition_facts'] = productItem?.enrichment?.nutrition_facts;
    productsObjectsArray[index]['bullet_descriptions'] = productItem?.product_description?.bullet_descriptions;
    productsObjectsArray[index]['upc'] = productItem?.primary_barcode;
    productsObjectsArray[index]['dpci'] = productItem?.dpci;
    productsObjectsArray[index]['origin'] = productItem?.handling?.import_designation_description;

    fs.writeFileSync(
      `data/test_${index}_products_info_extraction.json`,
      // `data/product_${index}_info.json`,
      JSON.stringify(productsObjectsArray, null, 4), 
      'utf8'
    );
    // console.log(productJSON);
  }
}


const index = 0;
fetchProductInfo(index);


/*
async.mapLimit(productsObjectsArray, 5, async function(productObject) {
  const url = productObject['url'];
  const response = await fetch(url);

  if (response.status == 200) {
    const htmlText = await response.text();
    const root = HTMLParser.parse(htmlText);
    const body = root.querySelector('body');

    // Attempt extraction of grocery group path via Target's "bread crumb links"
    try {
      const breadCrumbsLinks = Array.from(
        body.querySelectorAll('[data-test="@web/Breadcrumbs/BreadcrumbLink"]')
      ).map(e => {
        return e.innerText
          // Remove extra whitespace
          .trim().replace(/\s+/g, ' ')
          // Decode possibe special characters
          .replace(/\s&amp;\s/g, ' & ');
    });

      productObject['grocery_group_path'] = breadCrumbsLinks.reduce((a, b) => a + '/' + b);
    } catch (error) {
      logger.warning("Failed grocery group path extraction for:")
      logger.error(productObject)
      logger.error(error);
    }
    

    if (!body.innerHTML.includes(expectedStringInNonPaginatedProductsWebpageHTML)) {
      return { 'is_website_possibly_paginated' : true, ...productObject }
    }

    if (body.innerHTML.includes(expectedStringInPaginatedProductsWebpageHTML)) {
      return { 'is_website_possibly_paginated' : true, ...productObject }
    }
    
    logger.warn(`Found possibly non-paginated website: ${url}`)
    return { 'is_website_possibly_paginated' : false, ...productObject }
    }
    
  logger.warn(`GET request's response status was not 200 for url: ${url}`)
  return { 'is_website_possibly_paginated' : null, ...productObject }

}, (err, results) => {
  if (err) { logger.error(err); throw err;  }
  
  fs.writeFileSync(
    'data/urls_for_task_2.1.json',
    JSON.stringify(results, null, 2), 
    'utf8'
  );

  logger.info('Completed subtask')
});
*/

/*
  "tcin": 47868632,
  "original_tcin": 47868632,
  "dpci": "270-05-0488",
  "title": "Good Food Made Simple All Natural Bacon, Egg & Cheese Breakfast Frozen Burrito - 5oz",
  "url": "https://www.target.com/p/good-food-made-simple-all-natural-bacon-egg-cheese-breakfast-frozen-burrito-5oz/-/A-47868632",
  "image_url": "https://target.scene7.com/is/image/Target/GUEST_f8d34a4c-47ee-42c0-8fe1-aa21342926ef",
  "merged_bread_crumbs": "Target/Grocery/Frozen Foods/Frozen Single Serve Meals"
*/


// 'https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&tcin=47868632&is_bot=false&store_id=671&pricing_store_id=671&has_pricing_store_id=true&has_financing_options=true&include_obsolete=true&visitor_id=018EECDE90C702018E5EA8C77C7A126D&has_size_context=true&skip_personalized=true&skip_variation_hierarchy=true&channel=WEB&page=%2Fp%2FA-47868632'.split('&')

/*
# %%
tcin = 47868632
tcin = 13234505
'https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?' + '&'.join([
  'key=9f36aeafbe60771e321a7cc95a78140772ab3e96',
  f'tcin={tcin}', 
  # 'is_bot=false',  ## this does not seem necessary, but, ¿tal vez usarlo?
  # 'store_id=671', 
  'pricing_store_id=3991',  # DOES NOT SEEM TO REQUIRE CHANGE
  # 'has_pricing_store_id=true', 
  # 'has_financing_options=true', 
  # 'include_obsolete=true', 
  f'visitor_id=018EECDE90C702018E5EA8C77C7A{123}D', 
  # 'has_size_context=true', 
  # 'skip_personalized=true', 
  # 'skip_variation_hierarchy=true', 
  'channel=WEB', 
  f'page=%2Fp%2FA-{tcin}'
])

# %%
'https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&tcin=13234505&is_bot=false&store_id=671&pricing_store_id=671&has_pricing_store_id=true&has_financing_options=true&include_obsolete=true&visitor_id=018EECDE90C702018E5EA8C77C7A126D&has_size_context=true&skip_personalized=true&skip_variation_hierarchy=true&channel=WEB&page=%2Fp%2FA-13234505'.split('&')

# %%


  "tcin": 47868632,
  "original_tcin": 47868632,
  "dpci": "270-05-0488",
  "title": "Good Food Made Simple All Natural Bacon, Egg & Cheese Breakfast Frozen Burrito - 5oz",
  "url": "https://www.target.com/p/good-food-made-simple-all-natural-bacon-egg-cheese-breakfast-frozen-burrito-5oz/-/A-47868632",
  "image_url": "https://target.scene7.com/is/image/Target/GUEST_f8d34a4c-47ee-42c0-8fe1-aa21342926ef",
  "merged_bread_crumbs": "Target/Grocery/Frozen Foods/Frozen Single Serve Meals"



'https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2?key=9f36aeafbe60771e321a7cc95a78140772ab3e96', 
  'category=wdysv', 
  'channel=WEB', 
  'count=24', 
  'default_purchasability_filter=false', 
  'include_dmc_dmr=false', 
  'include_sponsored=true', 
  'new_search=false', 
  'offset=0', 
  'page=%2Fc%2Fwdysv', 
  'platform=desktop', 
  'pricing_store_id=3991', 
  'spellcheck=true', 
  'useragent=Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+HeadlessChrome%2F125.0.0.0+Safari%2F537.36', 
  'visitor_id=018FFE27DA950201BD7C09943D12B677', 
  'zip=15400'

  */