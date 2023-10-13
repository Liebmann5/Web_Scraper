import React from 'react';
import { Link } from 'react-router-dom';

import Main from '../layouts/Main';
import GithubInfo from '../components/GithubInfo';

const Index = () => (
  <Main
    description={"Nick's personal website. Soon to be the API apply program thing gateway."}
  >
    <article className="post" id="index">
      <header>
        <div className="title">
          <h2>Nicks Website you Bald Headed dunce</h2>
          {/* <h2><Link to="/">Under Construction</Link></h2> */}
          <p>Nick's personal website. Soon to be the API apply program thing gateway</p>
        </div>
        <GithubInfo />
      </header>
      <div className="webpage-contents">
        <p> Welcome to my website. Please feel free to read more <Link to="/about">about me</Link>,
          or you can check out my {' '}
          {/*<Link to="/resume">resume</Link>, {' '}
          <Link to="/projects">projects</Link>, {' '}
          view <Link to="/stats">site statistics</Link>, {' '}
  or <Link to="/contact">contact</Link> me.*/}
        </p>
        <p> Source available <a href="https://github.com/liebmann5/personal-site">here</a>.</p>
      </div>
    </article>
  </Main>
);

export default Index;
