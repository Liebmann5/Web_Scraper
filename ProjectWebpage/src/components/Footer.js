import React from 'react';
import '../static/css/Footer.scss'; // Assuming you have a Footer.scss file for styling

const Footer = () => (
  <footer className="footer">
    <div className="container footer-whole">
      <div className="content footer-visible">
        <p>
          Nick The Chick © 2023. All rights reserved.
        </p>
      </div>
    </div>
  </footer>
);

export default Footer;

/*
import React from 'react';
import PropTypes from 'prop-types';

const Footer = () => (
    <footer>
        <br />
        <div className="personal-portrait">
            <img src={data.portrait} />
        </div>

        <div className="legal-documentation" id="fiscal-year-budget">
            <span className="footer-middle">
                <p>Nicholas J. Liebmann</p>
                <p>Jurisdiction in the Court of Law and all that stuff Nerd</p>
                <p>
                    <a className="footer-sitemap" href={data.sitemap}>Sitemap</a>
                    |
                    <a className="footer-sitemap" href={data.lapd}>Polices</a>
                    |
                    <a className="footer-sitemap" href={data.cookies}>Cookies</a>
                </p>
            </span>
        </div>

        <div className="social-media-links">
            <span className="social-media-row">
                <span id="index-one">
                    <a className="facebook-link" href={data.link} target="_blank">
                        <span className={data.elementorScreenOnly}>Facebook-f</span>
                        <i className={data.facbookIcon} /> {/*class="fab fa-facebook-f*}
                    </a>
                </span>
                <span id="index-two">
                    <a className="twitter-link" href={data.link} target="_blank">
                        <span className={data.elementorScreenOnly}>Twitter</span>
                        <i className={data.twitterIcon} />
                    </a>
                </span>
                <span id="index-three">
                    <a className="youtube-link" href={data.link} target="_blank">
                        <span className={data.elementorScreenOnly}>Youtube</span>
                        <i className={data.youtubeIcon} />
                    </a>
                </span>
                <span id="index-four">
                    <a className="linkedin-link" href={data.link} target="_blank">
                        <span className={data.elementorScreenOnly}>Linkedin-in</span>
                        <i className={data.linkedinIcon} />
                    </a>
                </span>
            </span>
        </div>
    </footer>
);

export default Footer;
*/


