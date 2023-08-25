/*
    new concurrent mode API with createRoot
    https://www.dhiwise.com/post/deep-dive-into-react-concurrent-mode-exploring-key-features-and-use-cases
*/
import React from 'react';
import { createRoot, hydrateRoot } from 'react-dom/client';
import App from './App';

const rootElement = document.getElementById('root');

// See https://reactjs.org/docs/strict-mode.html
const StrictApp = () => (
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// hydrate is required by react-snap.
if (rootElement.hasChildNodes()) {
  hydrateRoot(rootElement, <StrictApp />);
} else {
  const root = createRoot(rootElement);
  root.render(<StrictApp />);
}
