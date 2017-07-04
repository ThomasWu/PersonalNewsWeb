import React, { PropTypes } from 'react';
import { Link } from 'react-router';
import './Base.css';
import Auth from '../Auth/Auth';

const Base = ({children}) => (
    <div>
        <nav className="nav-bar indigo lighten-1">
            <div className="nav-wrapper">
                <Link to="/" className="brand-logo">Tap News</Link>
                <ul id="nav-mobile" className="right">
                    { Auth.isUserAuthenticated() ?
                        (<div>
                            <li>{Auth.getEmail()}</li>
                            <li><Link to="/logout">Log out</Link></li>
                        </div>)
                        :
                        (<div>
                            <li><Link to="/login">Log in</Link></li>
                            <li><Link to="/signup">Sign up</Link></li>
                        </div>)
                    }
                </ul>
            </div>
        </nav>
        {children}
        <br />
    </div>
);

Base.propTypes = {
    children: PropTypes.object.isRequired
};

export default Base;