import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom'; // Import Link for routing
import '../static/css/SiteNavigation.scss';

const Navigation = ({ data }) => (
  <nav className="site-navigation">
    <ul>
      {data.map((item, index) => (
        <li key={index}>
          <Link to={item.link}>{item.webpage}</Link> {/* Use Link instead of button for routing */}
        </li>
      ))}
    </ul>
  </nav>
);

Navigation.propTypes = {
  data: PropTypes.arrayOf(
    PropTypes.shape({
      webpage: PropTypes.string.isRequired,
      link: PropTypes.string.isRequired,
    })
  ).isRequired,
};
