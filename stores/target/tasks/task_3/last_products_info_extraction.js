require('dotenv').config();

const { logger } = require('./src/instances.js');

const { sleep, randomFloatInRange } = require('./src/wait_generators.js');
const { groupedFilteredProductsArray } = require('./src/products_array_partitioner');
const { sequentialGETrequestsForGroup } = require('./src/sequential_get_requests_agent.js');

const fs = require("fs"); 
const async = require("async");

// Assign specified wait times between operations
const minSecondsWaitBetweenRequest = 1;
const maxSecondsWaitBetweenRequest = 2;

const minSecondsWaitBetweenGroups = 5;
const maxSecondsWaitBetweenGroups = 10;

logger.info('Started subtask')

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
  
  fs.writeFileSync(
    'grocery-products-info.json',
    JSON.stringify(results.flat(), null, 4), 
    'utf8'
  );

  logger.info('Completed subtask')
});
