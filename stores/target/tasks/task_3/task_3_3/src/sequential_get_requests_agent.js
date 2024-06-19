const { logger } = require('./instances.js');
const { sleep, randomFloatInRange } = require('./wait_generators.js');

const Math = require('mathjs');

// Execute, sequentially, asynchronous (GET requests) tasks
// Source: https://stackoverflow.com/a/58786416
const sequentialGETrequestsForGroup = async (productsGroup, secondsWaitRangeBetweenRequests) => {
  const GETrequestResults = [];

  for (let productObject of productsGroup) {
    const tcinOfProduct = productObject['tcin'].toString();

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
  
    const response = await fetch(GETRequesURL, {
      method: 'GET',
      headers: {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
      }
    });
    await sleep(randomFloatInRange(secondsWaitRangeBetweenRequests[0], secondsWaitRangeBetweenRequests[1]));

    if (response.status == 200) {
      try {
        const productJSON = await response.json();
  
        let productItem;
        if (productJSON['data']['product'].hasOwnProperty('children')) {
          if (productJSON['data']['product']['children'].some(productItem => productItem?.tcin === tcinOfProduct)) {
            productItem = productJSON['data']['product']['children']
              .filter(productItem => productItem?.tcin === tcinOfProduct)
              [0]
              ['item'];      
          } else {
            logger.error('Failed extraction of product children with matching tcin value');
            GETrequestResults.push(productObject);
            continue
          }
        } else {
          productItem = productJSON['data']['product']['item'];
        }
    
        productObject['nutrition_facts'] = productItem?.enrichment?.nutrition_facts;
        productObject['bullet_descriptions'] = productItem?.product_description?.bullet_descriptions;
        productObject['upc'] = productItem?.primary_barcode;
        productObject['dpci'] = productItem?.dpci;
        productObject['origin'] = productItem?.handling?.import_designation_description;
    
        logger.info(`Completed extraction attempt for product with tcin value ${tcinOfProduct}`)
      } catch (error) {
        logger.warn(`Tcin ${tcinOfProduct}: Failure in some step of product JSON info extraction`);
        logger.error(error);
      } finally {
        GETrequestResults.push(productObject);
        continue
      }
    }
  
    logger.warn(`GET request reponse status was ${response.status}, for url ${GETRequesURL}`)
    GETrequestResults.push(productObject);
  }

  return GETrequestResults;
}


module.exports = {
  sequentialGETrequestsForGroup : sequentialGETrequestsForGroup,
}
