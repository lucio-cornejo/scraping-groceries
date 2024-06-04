const fs = require("fs"); 
const async = require("async");
const HTMLParser = require('node-html-parser');

const log4js = require("log4js");
log4js.configure({
  appenders: { target: { 
    type: "fileSync", 
    filename: "logs/grocery_products_last_info_download.log",
    layout: { type: 'pattern', pattern: '%d-%c:[%p]: %m' },
  } },
  categories: { default: { appenders: ["target"], level: "info" } },
});
const logger = log4js.getLogger("target");


const productCategoryTreeCssSelector = '[data-test="@web/Breadcrumbs/BreadcrumbNav"]'

const specificationsSectionCssSelector = '[data-test="@web/site-top-of-funnel/ProductDetailCollapsible-Specifications"]';
const specificationsCssSelector = '[data-test="item-details-specifications"] > div';
// const productsUrlForDataAsJSON = 'https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&tcin=PRODUCT_TCIN_VALUE&pricing_store_id=1';
const productsUrlForDataAsJSON = 'https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key=a5ae7fb188e78581614e4909f407462d8392b977&tcin=PRODUCT_TCIN_VALUE&pricing_store_id=1';

const labelInfoSectionCssSelector = '[data-test="@web/site-top-of-funnel/ProductDetailCollapsible-LabelInfo"]';


const productsURLS = JSON.parse(fs.readFileSync('data/products_urls.json', 'utf8'));
// productsURLS.splice(4)

/*
const productsURLS = [{
  'url' : 'https://www.target.com/p/oscar-mayer-jalapeno-cheddar-hot-dogs-16oz/-/A-91001109#lnk=sametab',
  'url' : 'https://www.target.com/p/kidfresh-frozen-chicken-meatballs-16-45oz/-/A-85356048#lnk=sametab'
}]
*/


async.mapLimit(productsURLS, 3, async function(productURLS) {
    const response = await fetch(productURLS['url']);
    const htmlText = await response.text();

    const root = HTMLParser.parse(htmlText);
    logger.info(`Product url: ${productURLS['url']}`);
    const productNewlyExtractedInfo = {};

    // Extract product's category tree
    const categoryTree = root.querySelector(productCategoryTreeCssSelector);
    if (categoryTree == null) {
      logger.error("Failed to extract product's category tree")
      return null;
    }

    productNewlyExtractedInfo['category_path'] =  Array.from(categoryTree.querySelectorAll('ol li'))
      .map(li => li.innerText.trim())
      .reduce((a, b) => a + '/' + b)
      .replace(/\s&amp;\s/g, ' & ');

    // Extract product's specification 
    const specificationsSection = root.querySelector(specificationsSectionCssSelector);
    if (specificationsSection == null) {
      logger.error("Failed to extract product's specification section")
      return { 'url': productURLS['url'], ...productNewlyExtractedInfo };
    }

    const productSpecifications = specificationsSection.querySelector(specificationsCssSelector);
    if (!productSpecifications) {
      logger.error("Failed to extract product's specifications")
      
      // Try to fetch the product's UPC via some Target's API
      try {
        const productTcinValue = productURLS['url'].match(/(\d+)(?=#lnk=sametab)/g)[0];
        const productJsonUrl = productsUrlForDataAsJSON.replace('PRODUCT_TCIN_VALUE', productTcinValue);
        logger.info(productJsonUrl);
  
        const newResponse = await fetch(productJsonUrl);
        const newResponseJSON = await newResponse.json();

        logger.info(newResponseJSON);
        productNewlyExtractedInfo['upc'] = newResponseJSON.data.product.item.primary_barcode;
      } catch (error) {
        logger.error("Failed to fetch product's UPC");
        logger.error(error);
        return { 'url': productURLS['url'], ...productNewlyExtractedInfo };
      }
    } 

    // Extract product's label info
    const labelInfoSection = root.querySelector(labelInfoSectionCssSelector);
    if (labelInfoSection == null) return { 'url': productURLS['url'], ...productNewlyExtractedInfo };

    productNewlyExtractedInfo['label_info'] = labelInfoSection.innerHTML;
    return { 'url': productURLS['url'], ...productNewlyExtractedInfo }
}, (err, results) => {
    if (err) { logger.error(err); throw err;  }
    
    fs.writeFileSync(
      'data/products_info.json',
      JSON.stringify(results.filter(e => e !== null), null, 4), 
      'utf8'
  );
});
