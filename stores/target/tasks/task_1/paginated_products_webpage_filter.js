const fs = require("fs"); 
const async = require("async");
const HTMLParser = require('node-html-parser');

const log4js = require("log4js");
log4js.configure({
  appenders: { target: { 
    type: "fileSync", 
    filename: "logs/task-1.2.log",
    layout: { type: 'pattern', pattern: '%d-%c:[%p]: %m' },
  } },
  categories: { default: { appenders: ["target"], level: "info" } },
});
const logger = log4js.getLogger("target");
logger.info('Started subtask')


const productsObjectsArray = JSON.parse(fs.readFileSync('data/urls_for_task_1.2.json', 'utf8'));

const expectedStringInNonPaginatedProductsWebpageHTML = "@web/slingshot-components/bubcat";
const expectedStringInPaginatedProductsWebpageHTML = "@web/site-top-of-funnel/ProductCardPlaceholder";


async.mapLimit(productsObjectsArray, 5, async function(productObject) {
  const url = productObject['url'];
  const response = await fetch(url);

  if (response.status == 200) {
    const htmlText = await response.text();
    const root = HTMLParser.parse(htmlText);
    const body = root.querySelector('body');

    if (!body.innerHTML.includes(expectedStringInNonPaginatedProductsWebpageHTML)) {
      return { 'is_website_possibly_paginated' : true, 'url' : url }
    }

    if (body.innerHTML.includes(expectedStringInPaginatedProductsWebpageHTML)) {
      return { 'is_website_possibly_paginated' : true, 'url' : url }
    }
    
    logger.warn(`Found possibly non-paginated website: ${url}`)
    return { 'is_website_possibly_paginated' : false, 'url' : url }
    }
    
  logger.warn(`GET request's response status was not 200 for url: ${url}`)
  return { 'is_website_possibly_paginated' : null, 'url' : url }

}, (err, results) => {
  if (err) { logger.error(err); throw err;  }
  
  fs.writeFileSync(
    'data/urls_for_task_2.1.json',
    JSON.stringify(results, null, 2), 
    'utf8'
  );

  logger.info('Completed subtask')
});
