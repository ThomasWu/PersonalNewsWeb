const mongoose = require('mongoose');

module.exports.connect = (uri) => {
    console.log('[MongoDB]', 'Connecting to', uri);
    mongoose.connect(uri);

    mongoose.connection.on('error', (err) => {
        console.log('Mongoose connction error %{err}');
        process.exit(-1);
    });

    // load models
    require('./user');
};