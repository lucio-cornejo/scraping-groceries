require('dotenv').config();

const { logger } = require('./src/instances.js');

const { sleep, randomFloatInRange } = require('./src/wait_generators.js');

const fs = require("fs"); 
const async = require("async");
const HTMLParser = require('node-html-parser');

logger.info('Started subtask')

// Assign specified wait times between operations
const minSecondsWaitBetweenRequest = 0;
const maxSecondsWaitBetweenRequest = 1;

const productsObjectsArray = JSON.parse(
  fs.readFileSync('products_urls_for_task_3.3.json', 'utf8')
);

async.mapLimit(productsObjectsArray, 20, async function(productObject) {
  const productUrl = productObject['url'];
  const productTcin = productObject['tcin'];

  logger.info(`tcin: ${productTcin}`);

  const productResult = {};
  productResult['url'] = productUrl;

  try {
    const response = await fetch(productUrl, {
      method: 'GET',
      headers: {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
      }
    });
    
    const htmlText = await response.text();
    const root = HTMLParser.parse(htmlText);
  
    const productJsonText = [...root.querySelectorAll('body script')]
      .filter(e => e.innerText.includes('__TGT_DATA__'))[0]
      .innerText
      .split('\n')
      .filter(codeLine => codeLine.includes('__TGT_DATA__'))[0]
      .replace(/\\"/g, '"');

    
    let productItem;
    const productJSON = {}

    if (productJsonText.includes('"item":')) {
      productJSON['item'] = JSON.parse(productJsonText
        .split('\n')
        .filter(codeLine => codeLine.includes('__TGT_DATA__'))[0]
        .replace(/\\"/g, '"')
        .split('"item":')
        .filter(text => text.includes('primary_barcode'))[0]
        .split('"product_classification"')[0]
        .slice(0, -1) + '}'
      );
      productItem = productJSON['item'];
    } else {
      if (!productJsonText.includes('"children":')) {
        logger.error(`Failed extraction of product item, for product url ${productUrl}`);
        return { ...productResult, was_extraction_successful: true }
      }

      productJSON['children'] = JSON.parse(productJsonText
        .split('\n')
        .filter(codeLine => codeLine.includes('__TGT_DATA__'))[0]
        .replace(/\\"/g, '"')
        .split('"children":')
        .at(-1)
        .split('"product_classification"')[0]
        .slice(0, -1) + '}}]'
      );

      if (productJSON['children'].some(productItem => productItem?.tcin === productTcin)) {
        productItem = productJSON['children']
          .filter(productItem => productItem?.tcin === productTcin)
          [0]
          ['item'];      
      } else {
        logger.error(`Failed extraction of product children with matching tcin value, for product url ${productUrl}`);
        return { ...productResult, was_extraction_successful: true }
      }
    }

    // At this point, the product item Object has been extracted
    productResult['nutrition_facts'] = productItem?.enrichment?.nutrition_facts;
    productResult['upc'] = productItem?.primary_barcode;
    productResult['dpci'] = productItem?.dpci;

    return { ...productResult, was_extraction_successful: true }
  } catch (e) {
    logger.warn(`Product info JSON failed for product url ${productUrl}, due to error ${e}`)
    return { ...productResult, was_extraction_successful: false }
  } finally {
    await sleep(randomFloatInRange(minSecondsWaitBetweenRequest, maxSecondsWaitBetweenRequest));
  }
}, (err, results) => {
  if (err) { logger.error(err); throw err;  }
  fs.writeFileSync(
    'data/test_products_info_extraction_via_product_url.json', 
    JSON.stringify(results, null, 2), 
    'utf8'
  );

  logger.info('Completed subtask')
});
