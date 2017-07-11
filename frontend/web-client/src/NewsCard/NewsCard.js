import React from 'react';
import no_image from './no-image-available.png';
import './NewsCard.css';

import Auth from '../Auth/Auth';

class NewsCard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            like_status: 0
        };
    }

    redirectToUrl(url) {
        this.sendClickLog();
        window.open(url, '_blank');
    }

    sendClickLog() {
        let url = `http://localhost:3000/news/userId/${Auth.getEmail()}/click/${this.props.news.digest}`;
        let request = new Request(encodeURI(url), {
            method: 'POST',
            headers: {
                'Authorization': 'bearer ' + Auth.getToken(),
            },
            cache: false
        });
        fetch(request);
    }

    render() {
        return (
            <div className="news-container">
                <div className="row">
                    <div className="col s4 fill">
                        <img src={this.props.news.urlToImage || no_image} alt='news-image' />
                    </div>
                    <div className="col s8">
                        <div className="news-intro-col">
                            <div className="news-intro-panel">
                                <h4 className="header"
                                    onClick={(e) => {e.preventDefault(); this.redirectToUrl(this.props.news.url);}}>
                                    {this.props.news.title}
                                </h4>
                                <div>
                                    <p className="caption">{this.props.news.description}</p>
                                </div>
                                <div className="row">
                                    <div className="col right">
                                        {this.props.news.source != null && <div className="chip light-blue news-chip">{this.props.news.source}</div>}
                                        {this.props.news.reason != null && <div className="chip light-green news-chip">{this.props.news.reason}</div>}
                                        {this.props.news.time != null && <div className="chip amber news-chip">{this.props.news.time}</div>}
                                    </div>
                                    <div className="col left">
                                        <button className="btn-floating btn-flat"
                                            onClick={(e) => {
                                                e.preventDefault();
                                                let like_status = this.state.like_status;
                                                if (like_status != 1) {
                                                    this.setState({
                                                        like_status: 1
                                                    });
                                                } else {
                                                    this.setState({
                                                        like_status: 0
                                                    });
                                                }
                                            }}>
                                            <i className={'material-icons ' + ((this.state.like_status == 1 && 'green-text') || (this.state.like_status != 1 && 'grey-text'))}>
                                                thumb_up
                                            </i>
                                        </button>
                                        <button className="btn-floating btn-flat"
                                            onClick={(e) => {
                                                e.preventDefault();
                                                let like_status = this.state.like_status;
                                                if (like_status != 2) {
                                                    this.setState({
                                                        like_status: 2
                                                    });
                                                } else {
                                                    this.setState({
                                                        like_status: 0
                                                    });
                                                }
                                            }}>
                                            <i className={'material-icons ' + ((this.state.like_status == 2 && 'red-text') || (this.state.like_status != 2 && 'grey-text'))}>
                                                thumb_down
                                            </i>
                                        </button>
                                        <button className="btn-floating btn-flat"
                                            onClick={(e) => {
                                                this.props.hideNews(this.props.news);
                                            }}>
                                            <i className="material-icons grey-text">
                                                delete
                                            </i>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default NewsCard;