import React from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import '../../static/css/SiteNavigation.scss';

const Navigation = ({ routes }) => (
  <nav className="navigation">
    <ul className="navigation-list">
      {routes.map((route, index) => (
        <li key={index} className="navigation-item">
          <Link to={route.path} className="navigation-link">
            {route.name}
          </Link>
        </li>
      ))}
    </ul>
  </nav>
);

Navigation.propTypes = {
  routes: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      path: PropTypes.string.isRequired,
    })
  ).isRequired,
};

export default Navigation;
