const express = require('express');
const router = express.Router();
const passport = require('passport');
const validator = require('validator');

router.post('/signup', (req, res, next) => {
    console.log('[Auth route]');
    const validationResult = validateSignupForm(req.body);
    if (!validationResult.success) {
        console.log('[Auth route]','validation failed');
        return res.status(400).json({
            success: false,
            message: validationResult.message,
            errors: validationResult.errors
        });
    }
    return passport.authenticate('local-signup', (err) => {
        if (err) {
            console.log('[Auth route]',err);
            // check if Mongo DB error
            if (err.name === 'MongoError' && err.code === 11000) {
                return res.status(409).json({
                    success: false,
                    message: 'Check the form for wrong inputs.',
                    errors: {
                        email: 'This email is already taken.'
                    }
                });
            } 
            // other errors
            return res.status(400).json({
                success: false,
                message: 'Could not process the signup request.'
            });
        }
        console.log('[Auth route]', 'Succeed');
        return res.status(200).json({
            success: true,
            message: 'Signup succeeded'
        });
    })(req, res, next);
});

router.post('/login', (req, res, next) => {
    const validationResult = validateLoginForm(req.body);
    if (!validationResult.success) {
        return res.status(400).json({
        success: false,
        message: validationResult.message,
        errors: validationResult.errors
        });
    }

    return passport.authenticate('local-login', (err, token, userData) => {
        if (err) {
            if (err.name === 'IncorrectCredentialsError') {
                return res.status(400).json({
                success: false,
                message: err.message
                });
            }

            return res.status(400).json({
                success: false,
                message: 'Could not process the form: ' + err.message
            });
        }

        return res.json({
            success: true,
            message: 'You have successfully logged in!',
            token,
            user: userData
        });
    })(req, res, next);
});

function validateSignupForm(payload) {
    console.log(payload);
    const errors = {};
    let isFormValid = true;
    let message = '';

    if (!payload || typeof payload.email !== 'string' || !validator.isEmail(payload.email)) {
        isFormValid = false;
        errors.email = 'Please provide a correct email address.';
    }

    if (!payload || typeof payload.password !== 'string' || payload.password.trim().length < 8) {
        isFormValid = false;
        errors.password = 'Password must have at least 8 characters.';
    }

    if (!isFormValid) {
        message = 'Check the form for errors.';
    }

    return {
        success: isFormValid,
        message,
        errors
    };
}

function validateLoginForm(payload) {
    console.log(payload);
    const errors = {};
    let isFormValid = true;
    let message = '';

    if (!payload || typeof payload.email !== 'string' || payload.email.trim().length === 0) {
        isFormValid = false;
        errors.email = 'Please provide your email address.';
    }

    if (!payload || typeof payload.password !== 'string' || payload.password.trim().length === 0) {
        isFormValid = false;
        errors.password = 'Please provide your password.';
    }

    if (!isFormValid) {
        message = 'Check the form for errors.';
    }

    return {
        success: isFormValid,
        message,
        errors
    };
}

module.exports = router;