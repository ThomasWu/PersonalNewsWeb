var jayson = require('jayson');
const logger = require('../logger/logger');

const SECTION = 'rpc-client';
let log = (message) => {
    logger.log(SECTION, message);
}

var client = jayson.client.http({
    port: 4040,
    hostname: 'localhost'
});

// Testing method
function add(a, b, callback) {
    client.request('add', [a, b], function(err, error, response) {
        if (err) throw err;
        console.log(response);
        callback(response);
    });
}

// Get news summaries for a user
function getNewsSummariesForUser(user_id, page_num, callback) {
    client.request('getNewsSummariesForUser', 
        [user_id, page_num], 
        function(err, error, response) {
            if (err) {
                log(`Get news failed for ${user_id}`);
                throw err;
            }
            console.log(response);
            callback(response);
        }
    );
}

// Log a user's click event on a news
function logNewsClickForUser(user_id, news_id) {
    client.request('logNewsClickForUser', [user_id, news_id], null, function(err) {
            if (err) {
                log(`Log ${user_id} click failed`);
                throw err;
            }
        }
    );
}

// Log a user's like/dislike/hide action on a news
function logNewsPreferenceForUser(user_id, news_id, prefer_status) {
    client.request('logNewsPreferenceForUser', [user_id, news_id, prefer_status], null, function(err) {
            if (err) {
                log(`Log ${user_id} preference failed`);
                throw err;
            }
        }
    );
}

module.exports = {
    add: add,
    getNewsSummariesForUser: getNewsSummariesForUser,
    logNewsClickForUser: logNewsClickForUser,
    logNewsPreferenceForUser: logNewsPreferenceForUser
};