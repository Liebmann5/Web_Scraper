// C:\Users\user\OneDrive\Documents\GitHub\Web_Scraper\ProjectWebpage\src\components\Troubleshoot.js

import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';

const Home = () => <div>Home</div>;
const About = () => <div>About</div>;

const Troubleshoot = () => {
  return (
    <div>
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/about">About</Link>
          </li>
        </ul>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </div>
  );
};

export default Troubleshoot;


// import React from 'react';
// import { Helmet, HelmetProvider } from 'react-helmet-async';
// import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

// const Troubleshoot = () => {
//   return (
//     <HelmetProvider>
//       <BrowserRouter>
//         <Helmet>
//           <title>Troubleshooting Component</title>
//           <meta name='description' content='Troubleshooting React App' />
//         </Helmet>
//         <div>
//           <h1>Troubleshooting Component</h1>
//           <p>If you see this, React is working!</p>
//           <Routes>
//             <Route path='/' element={<Home />} />
//             <Route path='/test' element={<Test />} />
//           </Routes>
//           <nav>
//             <ul>
//               <li><Link to='/'>Home</Link></li>
//               <li><Link to='/test'>Test</Link></li>
//             </ul>
//           </nav>
//         </div>
//       </BrowserRouter>
//     </HelmetProvider>
//   );
// };

// const Home = () => <div><h2>Home</h2><p>React Router is working if you see this.</p></div>;
// const Test = () => <div><h2>Test</h2><p>React Router is working if you see this too.</p></div>;

// export default Troubleshoot;