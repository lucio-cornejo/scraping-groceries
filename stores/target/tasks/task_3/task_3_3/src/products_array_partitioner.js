require('dotenv').config();

const fs = require('fs');

const filterAndGroupFetchedProductsArray = (groupSize) => {
  const arrayFirstIndex = parseInt(process.env.PRODUCTS_JSON_LIST_FIRST_INDEX);
  const arrayLastIndex = parseInt(process.env.PRODUCTS_JSON_LIST_LAST_INDEX);

  // Filter by indices "i" which satisfy arrayFirstIndex <= i < arrayLastIndex .
  const productsObjectsArray = JSON.parse(
    // unique_products_urls_JSON_string
    fs.readFileSync('products_urls_for_task_3.3.json', 'utf8')
  ).filter((productObject, index) => (index >= arrayFirstIndex ) && (index < arrayLastIndex));


  // const groupSize = 5;
  const numberOfProducts = productsObjectsArray.length;

  // Perform modulo operation in JavaScript
  // Source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Remainder
  const remainder = ((numberOfProducts % groupSize) + groupSize) % groupSize;

  const indicesOfGroupsFirstItem = Array.from(
    Array(1 + ((numberOfProducts - remainder - groupSize) / groupSize)).keys()
  ).map(e => groupSize * e);


  const indicesPerGroup = indicesOfGroupsFirstItem
    .map(firstGroupItemIndex => {
      return Array.from(Array(groupSize).keys()) 
        .map(indexShift => indexShift + firstGroupItemIndex)
    });

  // Add possibly pending indices to array of groups items indices
  if (remainder !== 0) {
    indicesPerGroup.push(
      Array.from(Array(remainder).keys())
      .map(indexShift => indexShift + numberOfProducts - remainder)
    );
  }

  const groupedProductsArray = indicesPerGroup
    .map(groupItemsIndices => groupItemsIndices.map((index) => productsObjectsArray[index]));

  return groupedProductsArray;
};


module.exports = {
  filterAndGroupFetchedProductsArray : filterAndGroupFetchedProductsArray,
}
