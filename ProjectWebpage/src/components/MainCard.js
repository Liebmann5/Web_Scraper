import React from 'react';
import PropTypes from 'prop-types';

// THIS IS RELATED TO projects.js !!!! (This file is basically just a cell holding cells -> ??SubCard.js??)
const Card = ({ data }) => (
    <div className="main-card">
        <figure className="main-card-attr">
            <a href={data.link} className="main-card-img">
                <img src={data.link} alt={data.alt} />
            </a>
            <div className="summary">
                <h3><a href={data.link}>{data.title}</a></h3>
                <p>{data.summary}</p>
            </div>
        </figure>
    </div>
);

Card.propTypes = {
    data: PropTypes.shape({
        title: PropTypes.string.isRequired,
        link: PropTypes.string,
        image: PropTypes.string.isRequired,
        alt: PropTypes.string.isRequired,
        summary: PropTypes.string.isRequired,
    }).isRequired,
};

export default Card;
