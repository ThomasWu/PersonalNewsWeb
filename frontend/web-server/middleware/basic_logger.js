const logger = require('../logger/logger');

module.exports = (req, res, next) => {
    let message = `Received a request from ${req.ip}: (${req.url}).`;
    logger.log('webserver', message);
    next();
};