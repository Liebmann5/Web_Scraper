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
const AutoApply = lazy(() => import('./pages/Auto-Apply'));
const NotFound = lazy(() => import('./pages/NotFound'));

const App = () => (
    <BrowserRouter basename={PUBLIC_URL}>
        <Suspense fallback={<Main />}>
            <Routes>
            {/* <Banner /> */}
                {/* Commented out routes */}
                <Route path="/" element={<Index />} />
                <Route path="/about" element={<About />} />
                <Route path="/projects" element={<Projects />} />
                <Route path="/stats" element={<Stats />} />
                <Route path="/data" element={<Data />} />
                <Route path="/papers" element={<Papers />} />
                <Route path="/autoapply" element={<AutoApply />} />
                <Route path="*" element={<NotFound />} />
            </Routes>
        </Suspense>
        <Footer />
    </BrowserRouter>
);

export default App;
