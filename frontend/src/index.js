import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import './i18n'; // Your translation file
import { ThemeProvider } from '@mui/material/styles'; // 1. Import ThemeProvider
import theme from './theme'; // 2. Import our new theme

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    {/* 3. Wrap your App in the ThemeProvider */}
    <ThemeProvider theme={theme}>
      <App />
    </ThemeProvider>
  </React.StrictMode>
);

