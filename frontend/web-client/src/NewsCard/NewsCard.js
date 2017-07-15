/*global confirm*/
/*eslint no-restricted-globals: ["error", "confirm"]*/

import React from 'react';
import no_image from './no-image-available.png';
import './NewsCard.css';

import Auth from '../Auth/Auth';

class NewsCard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            like_status: props.news.liked || 0,
            to_be_deleted: false
        };
    }

    redirectToUrl(url) {
        this.sendClickLog();
        window.open(url, '_blank');
    }

    sendClickLog() {
        let url = `/news/userId/${encodeURIComponent(Auth.getEmail())}/click/${encodeURIComponent(this.props.news.digest)}`;
        let request = new Request(url, {
            method: 'POST',
            headers: {
                'Authorization': 'bearer ' + Auth.getToken(),
            },
            cache: false
        });
        fetch(request);
    }

    updateLikeStatus(user_action) {
        let like_status = user_action;
        if (this.state.like_status == user_action) {
            like_status = 0;
        }
        this.setState({
            like_status: like_status
        });
        this.sendPreferenceLog(like_status);
    }

    sendPreferenceLog(prefer_status) {
        let url = `/news/userId/${encodeURIComponent(Auth.getEmail())}/prefer/${encodeURIComponent(this.props.news.digest)}/${prefer_status}`;
        let request = new Request(url, {
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
                                                this.updateLikeStatus(1);
                                            }}>
                                            <i className={'material-icons ' + ((this.state.like_status == 1 && 'green-text') || 'grey-text')}>
                                                thumb_up
                                            </i>
                                        </button>
                                        <button className="btn-floating btn-flat"
                                            onClick={(e) => {
                                                e.preventDefault();
                                                this.updateLikeStatus(-1);
                                            }}>
                                            <i className={'material-icons ' + ((this.state.like_status == -1 && 'red-text') || 'grey-text')}>
                                                thumb_down
                                            </i>
                                        </button>
                                        <button className="btn-floating btn-flat"
                                            onClick={(e) => {
                                                let to_be_deleted = this.state.to_be_deleted;
                                                this.setState({
                                                    to_be_deleted: !to_be_deleted
                                                });
                                            }}>
                                            <i className="material-icons grey-text">
                                                delete
                                            </i>
                                        </button>
                                    </div>
                                </div>
                                {
                                    this.state.to_be_deleted && 
                                    <div className="row">
                                        <strong className="grey-text">Do you want to delete this news?</strong>
                                        <button className="btn-floating btn-flat"
                                            onClick={(e) => {
                                                    this.setState({
                                                    to_be_deleted: false
                                                });
                                            }}>
                                            <i className="material-icons red-text">
                                                clear
                                            </i>
                                        </button>
                                        <button className="btn-floating btn-flat"
                                            onClick={(e) => {
                                                this.sendPreferenceLog('-2');
                                                this.props.hideNews(this.props.news);
                                            }}>
                                            <i className="material-icons green-text">
                                                done
                                            </i>
                                        </button>
                                    </div>
                                }
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default NewsCard;