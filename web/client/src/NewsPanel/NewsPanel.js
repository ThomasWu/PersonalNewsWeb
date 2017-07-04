import React from 'react';
import './NewsPanel.css';

import Auth from '../Auth/Auth';
import _ from 'lodash';

import NewsCard from '../NewsCard/NewsCard';

class NewsPanel extends React.Component {
    constructor() {
        super();
        this.state = {
            news: null,
            pageNum: 1,
            loadedAll: false
        };
        this.handleScroll = this.handleScroll.bind(this);
    }

    componentDidMount() {
        this.loadMoreNews();
        this.loadMoreNews = _.debounce(this.loadMoreNews, 2000);
        window.addEventListener('scroll', this.handleScroll);
    }

    handleScroll() {
        let scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
        if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50)) {
            console.log('Loads more news');
            this.loadMoreNews();
        }
    }

    loadMoreNews() {
        if (this.state.loadedAll === true) {
            return;
        }

        let url = `http://localhost:3000/news/userId/${Auth.getEmail()}/pageNum/${this.state.pageNum}`;

        let request = new Request(url, {
            method: 'GET',
            headers: {
                'Authorization': 'bearer ' + Auth.getToken(),
            },
            cache: false
        });

        fetch(request)
            .then( res => res.json() )
            .then( news => {
                if ( !news || news.length === 0 ) {
                    this.setState({loadedAll: true});
                }

                this.setState({
                    news: this.state.news? this.state.news.concat(news): news,
                    pageNum: this.state.pageNum + 1
                });
            });
    }

    renderNews() {
        console.log(this.state);
        const news_list = this.state.news.map(function(news) {
            return (
                <a className="list-group-item" href="#">
                    <NewsCard news={news}/>
                </a>
            );
        });

        return (
        <div className="container-fluid">
            <div className='list-group'>
            {news_list}
            </div>
        </div>
        );
    }

    render() {
        return (
            <div>
                {this.state.news? this.renderNews(): 'Loading...'}
            </div>
        );
    }
}

export default NewsPanel;
