import React from 'react';
import PropTypes from 'prop-types';
import { Helmet, HelmetProvider } from 'react-helmet-async';
import GithubInfo from '../components/GithubInfo';
import Navigation from '../components/Template/Navigation';
import Footer from '../components/Footer';
// import Analytics from '../components/Template/Analytics';

const Main = (props) => (
    <HelmetProvider>
      {/* Uncomment when Analytics component is done! */}
      {/* <Analytics /> */}
      {/* Uncomment when made a ScrollToTop component */}
      {/* <ScrollToTop /> */}
      <Helmet titleTemplate="%s | Nick 0" defaultTitle="Nick 1" defer={false}>
        {props.title && <title>{props.title}</title>}
        <meta name="description" content={props.description} />
      </Helmet>
      <div id="wrapper">
        <Navigation />
        <div id="main">
          <article className="post">
            <header>
              <div className="title">
                <h2>Under Construction you Bald Headed dunce</h2>
                <p>{props.description}</p>
              </div>
              <GithubInfo />
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
