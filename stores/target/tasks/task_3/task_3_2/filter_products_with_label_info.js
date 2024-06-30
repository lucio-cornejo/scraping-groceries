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
    // local: { appenders: ['file', 'console'], level: 'info' },
    local: { appenders: ['file'], level: 'info' },
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

const expectedStringInProductWithLabelInfo = 'Label info';

const productsObjectsArray = JSON.parse(fs.readFileSync('data/unique_products_urls.json', 'utf8'));

async.mapLimit(productsObjectsArray, 20, async function(productObject) {
  const productUrl = productObject['url'];
  const productTcin = productObject['tcin'];

  logger.info(`tcin: ${productTcin}`);

  let isPossiblyValidUrl = true;
  try {
    const response = await fetch(productUrl);
    const productHtmlText = await response.text();

    isPossiblyValidUrl = productHtmlText.includes(expectedStringInProductWithLabelInfo);
  } catch (err) {
    logger.error(`Failed url check for product with tcin ${productTcin} and url ${productUrl}`);
  } finally {
    if (!isPossiblyValidUrl) {
      logger.warn(`Possibly not valid url for product with tcin ${productTcin} and url ${productUrl}`);
      return null;
    }
    
    await sleep(randomFloatInRange(0, 1));
    return productObject;
  }
}, (err, results) => {
  if (err) { logger.error(err); throw err;  }
  fs.writeFileSync(
    'data/products_urls_for_task_3.3.json', 
    JSON.stringify(results.filter(e => e !== null), null, 4), 
    'utf8'
  );

  logger.info('Completed subtask')
});
