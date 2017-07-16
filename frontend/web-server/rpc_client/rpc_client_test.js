var client = require('./rpc_client');

client.add('1', '2', function(response) {
    console.assert(response == '12');
});

client.getNewsSummariesForUser('111@111.com', '1', function(response) {
<<<<<<< HEAD
<<<<<<< 38602ce03eca34cd2f2380fded123b846d4c568a
    // console.assert(response == '12');
    console.log(response);
});
=======
    console.log(response);
});
>>>>>>> running version
=======
    console.log(response);
});
>>>>>>> d28b392a7a5c331139a21d24be073f6c7bc165ff
