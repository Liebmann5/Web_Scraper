import React from 'react';
import { Link } from 'react-router-dom';

import '../../static/css/Navigation.scss';
import routes from '../../data/routes';

// Navigation component to display the list of routes
const Navigation = () => (
  <div className="sidebar-whole">
    <div className="sidebar-visible">
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
    </div>
  </div>
);

export default Navigation;
