const fs = require("fs"); 
const async = require("async");
const HTMLParser = require('node-html-parser');

const log4js = require("log4js");
log4js.configure({
  appenders: { target: { type: "file", filename: "logs/grocery_products_info_download.log" } },
  categories: { default: { appenders: ["target"], level: "info" } },
});
const logger = log4js.getLogger("target");


const productCategoryTreeCssSelector = '[data-test="@web/Breadcrumbs/BreadcrumbNav"]'

const labelInfoSectionCssSelector = '[data-test="@web/site-top-of-funnel/ProductDetailCollapsible-LabelInfo"]';

const specificationsSectionCssSelector = '[data-test="@web/site-top-of-funnel/ProductDetailCollapsible-Specifications"]';
const specificationsCssSelector = '[data-test="item-details-specifications"] > div';

/*
const productsURLS = JSON.parse(fs.readFileSync('data/products_urls.json', 'utf8'));
productsURLS.splice(4)

*/
const productsURLS = [{
  'url' : 'https://www.target.com/p/oscar-mayer-jalapeno-cheddar-hot-dogs-16oz/-/A-91001109#lnk=sametab'
}]


async.mapLimit(productsURLS, 3, async function(productURLS) {
    const response = await fetch(productURLS['url']);
    const htmlText = await response.text();

    const root = HTMLParser.parse(htmlText);
    console.log(productURLS['url']);
    const productNewlyExtractedInfo = {};

    // Extract product's category tree
    const categoryTree = root.querySelector(productCategoryTreeCssSelector);
    if (categoryTree == null) {
      console.error("Failed to extract product's category tree")
      return null;
    }

    productNewlyExtractedInfo['category_path'] =  Array.from(categoryTree.querySelectorAll('ol li'))
      .map(li => li.innerText.trim())
      .reduce((a, b) => a + '/' + b)
      .replace(/\s&amp;\s/g, ' & ');

    // Extract product's specification 
    const specificationsSection = root.querySelector(specificationsSectionCssSelector);
    if (specificationsSection == null) {
      console.error("Failed to extract product's specification section")
      return { 'url': productURLS['url'], ...productNewlyExtractedInfo };
    }

    const productSpecifications = specificationsSection.querySelector(specificationsCssSelector);
    if (!productSpecifications) {
      console.error("Failed to extract product's specifications")
      return { 'url': productURLS['url'], ...productNewlyExtractedInfo };
    } 

    /*

    // Expected categories inner text (as regex pattern): "(\s*)categoryName(\s*):(\s+)categoryValue(\s*)"
    const specificationCategoriesAndValues = Array.from(
      specificationsSection.querySelectorAll('[data-test="item-details-specifications"] div:has(> b)')
    ).map(e => {
      return e.innerText
      .toLowerCase().trim()
      .split(':').map(text => text.trim())
    });
    const lowercasedSpecificationCategories = specificationCategoriesAndValues.map(e => e[0]);

    console.log(
      lowercasedSpecificationCategories
    )

    if (lowercasedSpecificationCategories.includes('upc')) {
      productNewlyExtractedInfo['upc'] = specificationCategoriesAndValues[
        lowercasedSpecificationCategories.indexOf('upc')
      ][1];
    } else if (lowercasedSpecificationCategories.includes('utc')) {
      productNewlyExtractedInfo['utc'] = specificationCategoriesAndValues[
        lowercasedSpecificationCategories.indexOf('utc')
      ][1];
    } else {
      return null;
    }
    
    // Extract product's label info
    const labelInfoSection = root.querySelector(labelInfoSectionCssSelector);
    if (labelInfoSection == null) return { 'url': productURLS['url'], ...productNewlyExtractedInfo };

    productNewlyExtractedInfo['label_info'] = labelInfoSection.innerHTML;

    return { 'url': productURLS['url'], ...productNewlyExtractedInfo }

    */
}, (err, results) => {
    if (err) throw err;
    
    console.log(results);
    fs.writeFileSync(
      'data/products_info.json',
      JSON.stringify(results.filter(e => e !== null), null, 4), 
      'utf8'
  );
});
