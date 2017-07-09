from news_api_client import NewsApiClient

NEWS_API_KEY = '695bc4c0157c49ceab9ccb45e78dc009'
NEWS_API_URL = 'https://newsapi.org/v1/articles'

# NEWS API sources
BBC_NEWS = 'bbc-news'
BBC_SPORT = 'bbc-sport'
BLOOMBERG = 'bloomberg'
CNN = 'cnn'
DAILY_MAIL = 'daily-mail'
ESPN = 'espn'
FT = 'financial-times'
GOOGLE_NEWS = 'google-news'
NYT = 'the-new-york-times'

DEFAULT_SOURCES = [CNN, BBC_NEWS, BBC_SPORT, BLOOMBERG, CNN, DAILY_MAIL, ESPN, FT, GOOGLE_NEWS, NYT]

def test_basic():
    client = NewsApiClient(
        sources=['bbc-news'], 
        apiKey=NEWS_API_KEY, 
        url=NEWS_API_URL)
    newNews = client.getNews()
    assert len(newNews) > 0
    # for news in newNews:
    #     print news['title']
    print 'test_basic passed'

if __name__ == '__main__':
    test_basic()
