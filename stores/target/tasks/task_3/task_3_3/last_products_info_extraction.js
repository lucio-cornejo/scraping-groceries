require('dotenv').config();

const { logger } = require('./src/instances.js');

const { sleep, randomFloatInRange } = require('./src/wait_generators.js');
const { filterAndGroupFetchedProductsArray } = require('./src/products_array_partitioner');
const { sequentialGETrequestsForGroup } = require('./src/sequential_get_requests_agent.js');
const { uploadJsonToS3 } = require('./src/aws_s3_bucket_updater.js');

const fs = require("fs"); 
const async = require("async");

// Assign specified wait times between operations
const minSecondsWaitBetweenRequest = 1;
const maxSecondsWaitBetweenRequest = 2;

const minSecondsWaitBetweenGroups = 5;
const maxSecondsWaitBetweenGroups = 10;

(async () => {
  logger.info('Started subtask')
  const groupedFilteredProductsArray = await filterAndGroupFetchedProductsArray();

// /*
async.mapLimit(groupedFilteredProductsArray, 4, async function(productsGroup) {
  logger.info("Started sequential fetch task for some group");

  const sequentialFetchesResult = await sequentialGETrequestsForGroup(
    productsGroup,
    [minSecondsWaitBetweenRequest, maxSecondsWaitBetweenRequest]
    // [minSecondsWaitBetweenGroups, maxSecondsWaitBetweenGroups]
  );

  await sleep(randomFloatInRange(minSecondsWaitBetweenGroups, maxSecondsWaitBetweenGroups));

  return sequentialFetchesResult;
}, (err, results) => {
  if (err) { logger.error(err); throw err;  }
  
  const StringifiedJsonData = JSON.stringify(results.flat(), null, 4);
  
  const s3_file_name = 'grocery-products-info-for-indices-range-' +
    process.env.PRODUCTS_JSON_LIST_FIRST_INDEX +
    '_' +
    process.env.PRODUCTS_JSON_LIST_LAST_INDEX +
    '.json';

  // Save locally
  // fs.writeFileSync(s3_file_name, StringifiedJsonData, 'utf8');
  
  uploadJsonToS3(
    process.env.S3_BUCKET_NAME,
    s3_file_name,
    StringifiedJsonData
  )

  logger.info('Completed subtask')
});
// */
})();
