import React, { Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Main from './layouts/Main'; //fallback for lazy pages

import './static/css/Main.scss';
import Footer from './components/Footer';
const { PUBLIC_URL } = process.env;

const Index = lazy(() => import('./pages/Index'));
const About = lazy(() => import('./pages/About'));
const Projects = lazy(() => import('./pages/Projects'));
const Stats = lazy(() => import('./pages/Stats'));
const Data = lazy(() => import('./pages/Data'));
const Papers = lazy(() => import('./pages/Papers'));
const NotFound = lazy(() => import('./pages/NotFound'));

const App = () => (
    <BrowserRouter basename={PUBLIC_URL}>
        <Suspense fallback={<Main />}>
            <Routes>
            {/* <Banner />
            ok roots being here makes sense b/c I was laying out the overall design BUT... 
            how do you put all your various pages here? You can't you dunce! SSSSSooooo direct
            them here you doofus dunce crook! */}
                {/* Commented out routes */}
                <Route path="/" element={<Index />} />
                <Route path="/about" element={<About />} />
                <Route path="/projects" element={<Projects />} />
                <Route path="/stats" element={<Stats />} />
                <Route path="/data" element={<Data />} />
                <Route path="/papers" element={<Papers />} />
                <Route path="*" element={<NotFound />} />
            </Routes>
        </Suspense>
        <Footer />
    </BrowserRouter>
);

export default App;



// // Import necessary modules
// import React, { useEffect, useRef } from 'react';

// // Sidebar component
// const Sidebar = () => {
//   // Reference to the sidebar DOM element
//   const sidebarRef = useRef(null);

//   // Check 1: Verifies if the Sidebar Component is being rendered
//   useEffect(() => {
//     console.log("Check 1: Sidebar component is being rendered.");

//     // Check 2: Verifies if Sidebar is visible in the DOM
//     if (sidebarRef.current) {
//       console.log("Check 2: Sidebar is visible in the DOM.");
//     } else {
//       console.log("Check 2: Sidebar is NOT visible in the DOM.");
//     }

//     // Check 3: Verifies if Sidebar CSS is being applied correctly
//     const computedStyle = window.getComputedStyle(sidebarRef.current);
//     if (computedStyle) {
//       console.log("Check 3: Sidebar CSS is being applied.", computedStyle);
//     } else {
//       console.log("Check 3: Sidebar CSS is NOT being applied.");
//     }

//   }, []);

//   return (
//     <div ref={sidebarRef} id="sidebar" className="sidebar">
//       <p>Sidebar content</p>
//     </div>
//   );
// };

// // Main App component
// const App = () => {
//   // Check 5: Manually check the browser console for any errors or warnings
//   // Check 6: Manually inspect for any global CSS that might be affecting the Sidebar using browser DevTools
//   // Check 4: Manually inspect if Sidebar is in the component tree using React DevTools

//   return (
//     <div className="app">
//       <Sidebar />
//     </div>
//   );
// };

// export default App;
