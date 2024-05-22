# Web Scraper: Automate Your Job Search

Welcome to the Web Scraper project, a cutting-edge solution designed to transform the way you approach the job market. By harnessing the power of machine learning and artificial intelligence with SpaCy & EleutherAI, this tool almost completely automates the entire job application process, making it more efficient and significantly less time-consuming.

## Features

- **Automated Job Searching**: Leverages SpaCy AI to identify job openings that match your skills and interests.
- **Intelligent Application Process**: Automatically fills out application forms with unique, personalized responses.
- **Security Bypass Capabilities**: Uses OxyLabs solutions to navigate around common web scraping hurdles, such as CAPTCHAs and IP bans.
- **Market Insights**: Integrates with FastAPI and MariaDB for backend operations, providing real-time job market analytics through Google Sheets.

## Quick Start

### Installation

First, clone the repository to your local machine and navigate to the project directory:

```bash
git clone https://github.com/Liebmann5/Web_Scraper.git
cd Web_Scraper
```
For MAC users:

```bash
sh setup.sh
```
For Windows users:

```cmd
setup.bat
```
Press **ENTER**

That's it! The program should be ready to go!

## How It Works

On the first run, you'll be prompted to enter details such as your resume, social security number, other basic personal information, and a unique career summary. Web_Scraper then takes over, using sophisticated algorithms like [point-slope formula](https://en.wikipedia.org/wiki/Linear_equation), to find and apply to jobs that not only match your qualifications but also your career aspirations.

## AutoApply - The Heart of Automation

The AutoApply module is central to the Web Scraper, encompassing several components each tailored to streamline specific aspects of the job application process:

- **JobSearchWorkflow.py**: Coordinates the overall workflow.
- **UsersFirstUse.py**: Collects initial user data for a personalized experience.
- **ManageUserJobSearch.py**: Tailors job search based on user's technology preferences.
- **GoogleSearch.py**: Automates web searches for relevant job openings.
- **CompanyOpeningsAndApplications.py**: Handles the application process, from finding openings to submitting applications.

## Workflow Overview & Diagram

The AutoApply program follows this streamlined process:

`JobSearchWorkflow.py > GoogleSearch.py > JobSearchWorkflow.py > CompanyOpeningsAndApplications.py`

1. **Start with JobSearchWorkflow.py**: Initiates the job search.
2. **Proceed to GoogleSearch.py**: Finds relevant job openings.
3. **Return to JobSearchWorkflow.py**: Filters and Organizes found job openings.
4. **End with CompanyOpeningsAndApplications.py**: Applies to appropriately fit roles.

## Video Demonstration

[![Video Demo](https://github.com/Liebmann5/Web_Scraper/blob/main/Web_Scraper_Functionality_02-ezgif.com-video-to-gif-converter(1).gif)](https://pixeldrain.com/u/onnHYrVS)

## Follow Terminal Output

[![Follow Terminal Output](https://img.shields.io/badge/Terminal%20Output-Link-blue)](https://github.com/Liebmann5/Web_Scraper/blob/main/terminalOutput.txt)

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Stay Connected

For more information, questions, and updates, check out this [GitHub repository](https://github.com/Liebmann5/Web_Scraper) that leads you no where :P.

Thank you and now go do whatever the heck it is that you do!
