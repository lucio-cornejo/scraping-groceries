const log4js = require("log4js");

log4js.configure({
  appenders: { 
    console: { type: 'console' },
    cloudwatch: { type: 'console', layout: { type: 'basic' } },
    file: { 
      type: 'fileSync', 
      filename: 'task-3.3.log',
      layout: { type: 'pattern', pattern: '%d-%c:[%p]: %m' },
    } 
  },
  categories: { 
    default: { appenders: ['console'], level: 'info' },
    local: { appenders: ['file'], level: 'info' },
    // local: { appenders: ['file', 'console'], level: 'info' },
    production: { appenders: ['cloudwatch'], level: 'info' }
  },
});


module.exports = {
  getLogger : (loggerName) => log4js.getLogger(loggerName)
}