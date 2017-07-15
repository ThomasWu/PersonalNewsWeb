const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const config = require('../config/config.json');
const logger = require('../logger/logger');

const SECTION = 'auth-checker';
let log = (message) => {
    logger.log(SECTION, message);
}

module.exports = (req, res, next) => {
    console.log('auth_checker: req: ' + req.headers);

    if (!req.headers.authorization) {
        return res.status(401).end();
    }

    const token = req.headers.authorization.split(' ')[1];
    console.log('auth_check: token: ' + token);

    return jwt.verify(token, config.jwtSecret, (err, decoded) => {
        if (err) {
            console.log('authentication failed');
            return res.status(401).end();
        }

        const id = decoded.sub;

        return User.findById(id, (userErr, user) => {
            if (userErr || !user) {
                return res.status(401).end();
            }

            return next();
        });
    });
};
