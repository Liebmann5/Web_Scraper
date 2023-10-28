import React from 'react';
import { Link } from 'react-router-dom';

import Main from '../layouts/Main';
import GithubInfo from '../components/GithubInfo';
import cautionTapeImage from '../static/images/NicePng_caution-tape.png';  // Import the image

const Index = () => (
  <Main
    description={"Nick's personal website. Soon to be the API thing gateway."}
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
          or you can check out my available {' '}
          <Link to="/privateparts">Private Parts</Link>!
          {/*<Link to="/resume">resume</Link>, {' '}
          <Link to="/projects">projects</Link>, {' '}
          view <Link to="/stats">site statistics</Link>, {' '}
  or <Link to="/contact">contact</Link> me.*/}
        </p>
        <p> Source available <a href="https://scontent-hou1-1.xx.fbcdn.net/v/t1.6435-9/95605713_10218995949062272_8965093280861650944_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=dd63ad&_nc_ohc=yO2l7v8_ax0AX8WzU9W&_nc_ht=scontent-hou1-1.xx&oh=00_AfA_auB7sTHF4q4rtobSHu4hvwZlyTBme80Gl4iwx1NeZg&oe=655201DB">here</a>.</p>
        <div className="construction">
          <img src={cautionTapeImage} alt="First banner" className="first-banner" />
          {/* <img src="path/to/your/second-banner-image.jpg" alt="Second banner" className="second-banner" />
          <span className="construction-sign">Under Construction</span> */}
        </div>
      </div>
    </article>
  </Main>
);

export default Index;
