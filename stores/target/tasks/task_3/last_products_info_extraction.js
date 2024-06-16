const fs = require("fs"); 
const Math = require('mathjs');
const async = require("async");

const log4js = require("log4js");
log4js.configure({
  appenders: { target: { 
    type: "fileSync", 
    filename: "logs/task-3.2.log",
    layout: { type: 'pattern', pattern: '%d-%c:[%p]: %m' },
  } },
  categories: { default: { appenders: ["target"], level: "info" } },
});
const logger = log4js.getLogger("target");
logger.info('Started subtask')


const productsObjectsArray = JSON.parse(fs.readFileSync('data/unique_products_urls.json', 'utf8'));
productsObjectsArray.splice(10);

async.mapLimit(productsObjectsArray, 4, async function(productObject) {
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

  const response = await fetch(GETRequesURL);

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

    productObject['nutrition_facts'] = productItem?.enrichment?.nutrition_facts;
    productObject['bullet_descriptions'] = productItem?.product_description?.bullet_descriptions;
    productObject['upc'] = productItem?.primary_barcode;
    productObject['dpci'] = productItem?.dpci;
    productObject['origin'] = productItem?.handling?.import_designation_description;

    logger.info(`Completed extraction attempt for product with tcin value ${tcinOfProduct}`)
    return productObject;
  }

  logger.warn(`GET request reponse status was ${response.status}, for url ${GETRequesURL}`)
  return null;

}, (err, results) => {
  if (err) { logger.error(err); throw err;  }
  
  fs.writeFileSync(
    'data/grocery-products-info.json',
    JSON.stringify(results.filter(e => e !== null), null, 4), 
    'utf8'
  );

  logger.info('Completed subtask')
});
