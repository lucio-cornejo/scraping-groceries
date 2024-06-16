require('dotenv').config();

const { getLogger } = require('./logger.js');


module.exports = {
  logger : getLogger(process.env.PROFILE),
}