import React, { useState, useEffect } from 'react';

const GithubInfo = () => {
  const [githubData, setGithubData] = useState(null);

  useEffect(() => {
    const fetchGithubData = async () => {
      try {
        const response = await fetch('https://api.github.com/repos/liebmann5/web_scraper');
        const data = await response.json();
        setGithubData(data);
      } catch (error) {
        console.error('Error fetching GitHub data:', error);
      }
    };

    fetchGithubData();
  }, []);

  if (!githubData) {
    return <div>Loading...</div>;
  }

  return (
    <div className="github-info">
      <a href={githubData.html_url} target="_blank" rel="noopener noreferrer">
        <img src={githubData.owner.avatar_url} alt="GitHub Logo" className="github-logo" />
      </a>
      <div className="github-details">
        <span className="username-repo">{githubData.full_name}</span>
        <span className="stars-forks">
          <span className="stars">Stars: {githubData.stargazers_count}</span>
          {' | '}
          <span className="forks">Forks: {githubData.forks_count}</span>
        </span>
      </div>
    </div>
  );
};

export default GithubInfo;
