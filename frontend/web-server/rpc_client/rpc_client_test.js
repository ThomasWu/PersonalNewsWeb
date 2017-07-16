var client = require('./rpc_client');

client.add('1', '2', function(response) {
    console.assert(response == '12');
});

client.getNewsSummariesForUser('111@111.com', '1', function(response) {
    // console.assert(response == '12');
    console.log('received');
});