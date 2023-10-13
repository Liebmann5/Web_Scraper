import React from 'react';
import { Link } from 'react-router-dom';
//import PropTypes from 'prop-types';
import '../../static/css/Navigation.scss';
import routes from '../../data/routes';

// Navigation component to display the list of routes
const Navigation = () => (
  <nav id="navigation-bar">
    {/* Display the index route */}
    <h1 className="navigation-title">
      {routes.filter((route) => route.index).map((route) => (
        <Link key={route.name} to={route.path}>{route.name}</Link>
      ))}
    </h1>
    {/* Display the other routes */}
    <ul className="navigation-links">
      {routes.filter((route) => !route.index).map((route) => (
        <li key={route.name} className="navigation-item">
          <Link to={route.path} className="navigation-link">{route.name}</Link>
        </li>
      ))}
    </ul>
  </nav>
);

export default Navigation;
