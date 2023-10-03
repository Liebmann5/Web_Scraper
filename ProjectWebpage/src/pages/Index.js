import React from 'react';
import { Link } from 'react-router-dom';

import Main from '../layouts/Main';

const Index = () => (
  <Main
    description={"Nick's personal website. Soon to be the API apply program thing gateway "}
  >
    <article className="post" id="index">
      <header>
        <div className="title">
          <h2><Link to="/">Under Construction</Link></h2>
          <p>
            Soon to be a webpage revolved around testing!
          </p>
        </div>
      </header>
      <p> Welcome to my website. Please feel free to read more <Link to="/about">about me</Link>,
        or you can check out my {' '}
        {/*<Link to="/resume">resume</Link>, {' '}
        <Link to="/projects">projects</Link>, {' '}
        view <Link to="/stats">site statistics</Link>, {' '}
or <Link to="/contact">contact</Link> me.*/}
      </p>
      <p> Source available <a href="https://github.com/liebmann5/personal-site">here</a>.</p>
    </article>
  </Main>
);

export default Index;