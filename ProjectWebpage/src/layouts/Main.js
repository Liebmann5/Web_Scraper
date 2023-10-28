import React from 'react';
import PropTypes from 'prop-types';
import { Helmet, HelmetProvider } from 'react-helmet-async';

import Navigation from '../components/Template/Navigation';
import Footer from '../components/Footer';
// import Analytics from '../components/Template/Analytics';

const Main = (props) => (
    <HelmetProvider>
      {/* Uncomment when Analytics component is done! */}
      {/* <Analytics /> */}
      {/* Uncomment when made a ScrollToTop component */}
      {/* <ScrollToTop /> */}
      <Helmet titleTemplate="%s | Nick is better than you!" defaultTitle="Nick L" defer={false}>
        {props.title && <title>{props.title}</title>}
        <meta name="description" content={props.description} />
      </Helmet>
      <div id="wrapper">
        <div className="header-whole">
          <div className="header-visible">
            <Navigation />
          </div>
        </div>
        {/* <Navigation /> */}
        <div id="main">
          {props.children}
        </div>
        {props.fullPage ? null : <Footer />}
      </div>
    </HelmetProvider>
  );

Main.propTypes = {
  children: PropTypes.oneOfType([
     PropTypes.arrayOf(PropTypes.node),
     PropTypes.node,
  ]),
  fullPage: PropTypes.bool,
  title: PropTypes.string,
  description: PropTypes.string,
};

Main.defaultProps = {
  children: null,
  fullPage: false,
  title: null,
  description: "Nick's Private Website",
};

export default Main;
