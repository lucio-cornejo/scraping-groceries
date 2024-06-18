const fs = require('fs');
const async = require("async");
const log4js = require("log4js");

log4js.configure({
  appenders: { 
    console: { type: 'console' },
    cloudwatch: { type: 'console', layout: { type: 'basic' } },
    file: { 
      type: 'fileSync', 
      filename: 'logs/task-3.2.log',
      layout: { type: 'pattern', pattern: '%d-%c:[%p]: %m' },
    } 
  },
  categories: { 
    default: { appenders: ['console'], level: 'info' },
    local: { appenders: ['file', 'console'], level: 'info' },
    production: { appenders: ['cloudwatch'], level: 'info' }
  },
});

async function sleep (numSeconds) {
  return new Promise(r => setTimeout(r, 1000*numSeconds));
}

function randomFloatInRange (minValue, maxValue) {
  return parseFloat(
    (Math.random() * (maxValue - minValue) + minValue)
      // At most, keep two decimals
      .toFixed(2)
  );
} 

const logger =  log4js.getLogger('local');
logger.info("Started subtask");


const expectedStringInValidProductUrl = 'data-test="@web/Breadcrumbs/BreadcrumbLink"';
const expectedStringInNonValidProductUrl = 'data-test="productNotFound"';

const productsObjectsArray = JSON.parse(fs.readFileSync('data/unique_products_urls.json', 'utf8'));

async.mapLimit(productsObjectsArray, 10, async function(productObject) {
  const productUrl = productObject['url'];
  const productTcin = productObject['tcin'];

  logger.info(`tcin: ${productTcin}`);

  let isPossiblyValidUrl = null;

  try {
    const response = await fetch(productUrl);
    const productHtmlText = await response.text();

    if (productHtmlText.includes(expectedStringInNonValidProductUrl)) {
      isPossiblyValidUrl = false;
    } else {
      if (productHtmlText.includes(expectedStringInValidProductUrl)) {
        isPossiblyValidUrl = true;
      }
    }
  } catch (err) {
    logger.error(`Failed url check for product with tcin ${productTcin} and url ${productUrl}`);
  } finally {
    if (!isPossiblyValidUrl) {
      logger.warn(`Possibly not valid url for product with tcin ${productTcin} and url ${productUrl}`);
    }
    
    await sleep(randomFloatInRange(0, 1));
    return { ...productObject, "is_possibly_valid_url" : isPossiblyValidUrl }
  }
}, (err, results) => {
  if (err) { logger.error(err); throw err;  }
  fs.writeFileSync(
    'data/products_urls_for_task_3.3.json', 
    JSON.stringify(results, null, 4), 
    'utf8'
  );

  logger.info('Completed subtask')
});