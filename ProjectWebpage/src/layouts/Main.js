// https://github.com/staylor/react-helmet-async
// https://blog.sachinchaurasiya.dev/how-to-integrate-reactjs-and-react-helmet-async-manage-seo-and-meta-data
// https://blog.logrocket.com/search-optimized-spas-react-helmet/
// https://www.digitalocean.com/community/tutorials/react-react-helmet
/*import React from 'react'
import ReactDOM from 'react-dom'
import { Helmet, HelmetProvider } from 'react-helmet-async'

const main */
import React from 'react';
import PropTypes from 'prop-types';
import { Helmet, HelmetProvider } from 'react-helmet-async';
import GithubInfo from '../components/GithubInfo';
import SiteNavigation from '../components/SiteNavigation';
import Footer from '../components/Footer';
import Analytics from '../components/Template/Analytics';

const Main = (props) => (
    <HelmetProvider>
      <Analytics />
      {/* Uncomment when made a ScrollToTop component */}
      {/* <ScrollToTop /> */}
      <Helmet titleTemplate="%s | Nick" defaultTitle="Nick" defer={false}>
        {props.title && <title>{props.title}</title>}
        <meta name="description" content={props.description} />
      </Helmet>
      <div id="wrapper">
        <SiteNavigation />
        <div id="main">
          <article className="post">
            <header>
              <div className="title">
                <h2>Under Construction</h2>
                <p>{props.description}</p>
              </div>
            </header>
            {props.children}
          </article>
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
  description: "Default props description",
};

export default Main;
