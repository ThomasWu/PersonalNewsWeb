var client = require('./rpc_client');

client.add('1', '2', function(response) {
    console.assert(response == '12');
});

client.getNewsSummariesForUser('111@111.com', '1', function(response) {
<<<<<<< 38602ce03eca34cd2f2380fded123b846d4c568a
    // console.assert(response == '12');
    console.log(response);
});
=======
    console.log(response);
});
>>>>>>> running version
