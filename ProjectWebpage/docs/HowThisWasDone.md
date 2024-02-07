1. Found a basic goal -> https://asmen.icopy.site/
2. Created a index.html and styles.css file
3. Started making an outline for the webpage
   1. Erased everything and decided to plan
   2. Found this beautiful genius -> https://github.com/mldangelo/personal-site/tree/main
4. Static webpages can use JavaScript too remember!!
5. Apparently so can React...
   1. Read the genius's 'About': "My personal website - built with React, React-Router, React-Snap for Static-Export, and GitHub Pages."
   2. Also noticed the 'Languages' section had a lot of SCSS!!
6. NOTED: Everything important is in /src
   1. The /public had images for website and then an index.html file then a few ?MAYBE? other important files
      1. /public/index.html file appeared to be basic HTML outline BUT...  but did however have the <head> element completely filled in -> so that part is basically the same (?maybe noticed a few differeences here and there BUT feel that would be covered in React when I get there?)
   2. /docs useless unnecessary
   3. /.github this seemed to just have the GitHub Pages Hosting Webpage stuff
   4. project-name/ the rest of the files in here seemed like just normal technologies utilized documentation


Ready to Code
1. Make a directory and then give it a name that describes the project(This is the Holy of Holy's Folder)
2. Nerd made a /src directory so will do the same & also make a /README.md file
3. Make a /src/pages directory which should include a JavaScript file of all the different 'webpage options'!!! The headlines normally found in the header ?navigation bar?!!!
   1. NOTE: The main webpage is -> 'Index.js' !!!!!!!!
   2. NOTE: All the .js file names started with a capital letter!!


Stopped because I was actually ready to code but am an absolute fool and had no idea how to...
1. Review Genius's Tech Stack Documentation
   1. React-Router: *https://reactrouter.com/en/main/start/overview*
        -Feature Overview
            Client Side Routing
            React Router enables "client side routing".
    (This documentation is the absolute greatest definition of God-Tier!!!!)
    2. React:
       1. Quick Start - https://react.dev/learn
       2. Thinking in React - https://react.dev/learn/thinking-in-react
       3. Tutorial - https://react.dev/learn/tutorial-tic-tac-toe
    3. React-Snap
       1. GitHub - https://github.com/stereobooster/react-snap
            NOTE: "Pre-renders a web app into static HTML."
       2. DEV - https://dev.to/bryce/perform-a-react-disappearing-act-with-react-snap-1eo3
            NOTE: "Server-side rendering (SSR)"
       3. Blog - https://blog.logrocket.com/pre-rendering-react-app-react-snap/
2. I remembered why I hated React...   "JSX" -> https://react.dev/learn/writing-markup-with-jsx



Recognizing React and JSX
1. So React is just based around organization!! Best example of how everything is setup or how you will program and organize all your code is exactly like this box example -> https://react.dev/learn/thinking-in-react
2. Notice on his website the thin black lines everywhere!
3. Each section of the webpage, all seperated from each other by those thin black lines, all represent components which are just *'javascript with a little bit of HTML & CSS' = JSX*
4. By clicking on his 'Resume' tab scroll down and check out the 'Skills' section!
   1. Think about how he did it? Seems complex right?
        1. Everything is just pre-organized! Just like the Job project very tiny incremental methood tools!
        2. I COULD BE WRONG HERE but doubt it... so all that is going on here is the Russian Dolls thing! 'All' holds everything then the inner most doll or the 'bare-bones' most simplified classification of what he lists is 'Languages'!! SSSOOoooo the structure of order is probably like
   
 Python/JavaScript > Languages > Tools > Database > Data Science > Data Engineering > ALL

        The colors are also organized are also organized and most likely applied at the 2nd level(so 'Languages' in the structure of order above)! Start with the most basic skeleton and continue to build on to it!
        3. BAM! Expert level
        NOTE: In case I'm confused how to do the box around the topics in the 'Skills' section I believe it just is applied the background color always EXCEPT when the mouse hovers inside of it... then make the box and the words BLUE!!!

0. public/index.html
1. src/index.js
2. src/App.js
3. src/layouts/Main.js
4. src/pages/Resume.js
5. src/components/Resume/skills.js
6. src/components/Resume/Skills/CategoryButton.js
7. src/components/Resume/Skills/SkillBar.js
8. src/data/resume/skills.js
9. src/data/routes.js