import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom'; // Import Link for routing
import '../static/css/SiteNavigation.scss'; // Assuming you have a SiteNavigation.scss file for styling

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

export default Navigation;


/*
import React from 'react';
import PropTypes from 'prop-types';

*/

/*
  // Sample data for webpages
  const webpagesData = [
    { webpage: 'Home', link: '/home' },
    { webpage: 'About', link: '/about' },
    { webpage: 'Contact', link: '/contact' },
  ];
*/

/*

const Webpages = ({ data }) => (
    <ol>
        {data.map((item, index) => (
            <li key={index}>
                <button href={item.link}>{data.webpage}</button>
            </li>
        ))}
    </ol>
);

const Navigation = () => (
    <nav className="dropdown-webpages">
        <Webpages />
    </nav>
);

Webpages.propTypes = {
    data: PropTypes.arrayOf(
        PropTypes.shape({
            webpage: PropTypes.string.isRequired,
            link: PropTypes.string.isRequired,
        })
    ).isRequired,
};

export default Navigation;
*/