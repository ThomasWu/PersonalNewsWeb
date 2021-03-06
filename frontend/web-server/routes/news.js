var express = require('express');
var rpc_client = require('../rpc_client/rpc_client');
var router = express.Router();
const logger = require('../logger/logger');

const SECTION = 'news-route';
let log = (message) => {
    logger.log(SECTION, message);
}

router.get('/', function(req, res, next) {
    var news = [
        {
            'url':'http://us.cnn.com/2017/02/15/politics/andrew-puzder-failed-nomination/index.html',
            'title':"Inside Andrew Puzder's failed nomination",
            'description':"In the end, Andrew Puzder had too much baggage -- both personal and professional -- to be confirmed as President Donald Trump's Cabinet.",
            'source':'cnn',
            'urlToImage':'http://i2.cdn.cnn.com/cnnnext/dam/assets/170215162504-puzder-trump-file-super-tease.jpg',
            'digest':"3RjuEomJo26O1syZbU7OHA==\n",
            'reason':"Recommend"
        },
        {
            'title': 'Zero Motorcycles CTO Abe Askenazi on the future of two-wheeled EVs',
            'description': "Electric cars and buses have already begun to take over the world, but the motorcycle industry has been much slower to put out all-electric and hybrid models...",
            'url': "https://techcrunch.com/2017/03/23/zero-motorcycles-cto-abe-askenazi-on-the-future-of-two-wheeled-evs/",
            'urlToImage': "https://tctechcrunch2011.files.wordpress.com/2017/03/screen-shot-2017-03-23-at-14-04-01.png?w=764&h=400&crop=1",
            'source': 'techcrunch',
            'digest':"3RjuEomJo26O1syZbUdOHA==\n",
            'time':"Today",
            'reason':"Hot"
        }
    ];
    res.json(news);
});

router.get('/userId/:userId/pageNum/:pageNum', (req, res, next) => {
    user_id = req.params['userId'];
    page_num = req.params['pageNum'];
    console.log(`Fetching news for ${user_id} on page ${page_num}`);

    rpc_client.getNewsSummariesForUser(user_id, page_num, (response) => {
        log(`${user_id} successfully fetched news`);
        console.log('news received');
        res.json(response);
    });
})

// Log a user's click event
router.post('/userId/:userId/click/:newsId', function(req, res, next) {
    user_id = req.params['userId'];
    news_id = req.params['newsId'];
    console.log(`Logging click event on ${news_id} for ${user_id}`);
    
    log(`${user_id} cliked news ${news_id}`);
    rpc_client.logNewsClickForUser(user_id, news_id);
    res.status(200);
}); 

// Log a user's like/dislike/hide action on a news
router.post('/userId/:userId/prefer/:newsId/:prefer_status', function(req, res, next) {
    user_id = req.params['userId'];
    news_id = req.params['newsId'];
    prefer_status = req.params['prefer_status'];
    console.log(`Logging preference event on ${news_id} for ${user_id} with status ${prefer_status} (-2: hide, -1: dislike, 0: no preference, 1: like)`);
    log(`Logging preference event on ${news_id} for ${user_id} with status ${prefer_status} (-2: hide, -1: dislike, 0: no preference, 1: like)`);
    rpc_client.logNewsPreferenceForUser(user_id, news_id, prefer_status);
    res.status(200);
}); 

module.exports = router;