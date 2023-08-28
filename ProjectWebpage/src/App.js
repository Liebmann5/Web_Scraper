//0) https://legacy.reactjs.org/docs/code-splitting.html  |  https://react.dev/blog/2022/03/29/react-v18#new-suspense-features
//1) React.lazy
//2) Route-based code splitting
import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Route, Routes, Route } from 'react-router-dom';

import Main from './layouts/Main'; //fallback for lazy pages

const Home = lazy(() => import('./pages/Home'));
const About = lazy(() => import('./pages/About'));
const Projects = lazy(() => import('./pages/Projects'));
const Stats = lazy(() => import('./pages/Stats'));
const LiveData = lazy(() => import('./pages/LiveData'));
const Papers = lazy(() => import('./pages/Papers'));
const Index = lazy(() => import('./pages/Index'));

const App = () => {
    <BrowserRouter>
        <Suspense fallback={<Main />}>
            <Routes>
            {/* <Banner />
            ok roots being here makes sense b/c I was laying out the overall design BUT... 
            how do you put all your various pages here? You can't you dunce! SSSSSooooo direct
            them here you doofus dunce crook! */}
                <Route path="/" element={<Index />} />
                <Route path="/home" element={<Home />} />
                <Route path="/about" element={<About />} />
                <Route path="/projects" element={<Projects />} />
                <Route path="/stats" element={<Stats />} />
                <Route path="/live-data" element={<LiveData />} />
                <Route path="/papers" element={<Papers />} />
                <Route path="*/" element={<NotFound />} />
            </Routes>
        </Suspense>
    </BrowserRouter>
};

export default App;

// we need to send it to the DOM
// so we need to find and send it to the root then...
// have Babel render it son
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);