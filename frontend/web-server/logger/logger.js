const fs = require('fs');

const log_file = 'webserver.log';

function log(section, message) {
    const timestamp = new Date().toISOString().replace(/T/, ' ').replace(/\..+/, '');
    let log = `{"component": "webserver", "section":"${section}", "timestamp":"${timestamp}"Z, "message":"${message}"}\n`
    fs.appendFile(log_file, 
        log.replace(/\n/g, ''),
        function(err) {
            if (err) {
                console.log(err);
            }
        });
}

module.exports = {
    log: log
};