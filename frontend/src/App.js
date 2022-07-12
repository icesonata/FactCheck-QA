import './index.css';
import React from 'react';
import { HashRouter as Router } from 'react-router-dom';
import Routes from './routes/routes';
import 'bootstrap/dist/css/bootstrap.min.css';

export const App = () => {
  return (
    <Router hashType="noslash">
      <Routes />
    </Router>
  );
};
