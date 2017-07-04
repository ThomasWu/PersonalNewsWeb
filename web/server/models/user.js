const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const UserSchema = new mongoose.Schema({
    email: {
        type: String,
        index: {
            uniqure: true
        }
    },
    password: String,
});

UserSchema.methods.comparePassword = function comparePassword(password, callback) {
    console.log('[USER MODEL]', password, this.password);
    bcrypt.compare(password, this.password, callback);
};

UserSchema.pre('save', function saveHook(next) {
    const user = this;
    console.log('[USER MODEL]', 'User', user);

    if (!user.isModified('password')) return next();

    return bcrypt.genSalt((saltError, salt) => {
        if (saltError) {
            console.log('[USER MODEL]', 'Error',saltError);
            return next(saltError);
        }

        return bcrypt.hash(user.password, salt, (hashError, hash) => {
            if (hashError) {
                console.log('[USER MODEL]', 'Error',hashError);
                return next(hashError);
            }

            console.log('[USER MODEL]', 'Hash', hash);
            user.password = hash;

            return next();
        });
    });
});

module.exports = mongoose.model('User', UserSchema);