const fs = require('fs');

const log_file = 'webserver.log';

function log(section, message) {
    const timestamp = new Date().toISOString().replace(/T/, ' ').replace(/\..+/, '');
    fs.appendFile(log_file, 
        `{"component": "webserver", "section":"${section}", "timestamp":"${timestamp}"Z, "message":"${message}"}\n`,
        function(err) {
            if (err) {
                console.log(err);
            }
        });
}

module.exports = {
    log: log
};