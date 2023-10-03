const fs = require('fs');
const fetch = require('node-fetch');

const fetchGithubData = async () => {
  try {
    const response = await fetch('https://api.github.com/repos/liebmann5/web_scraper');
    const data = await response.json();
    fs.writeFileSync('./src/data/githubData.json', JSON.stringify(data));
  } catch (error) {
    console.error('Error fetching GitHub data:', error);
  }
};

fetchGithubData();
