import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Sidebar from './Sidebar';
import './App.css';
import Machine from './Machine.js';
import SJob from './Scheduled-jobs.js';
import Mail from './Admin-mail.js';
import CJob from './Completed-jobs.js';
import Software from './Software.js';
import Home from './Home.js';
import Inventory from './Inventory.js';
import '@fortawesome/fontawesome-free/css/all.min.css';


const App = () => {
  return (
    <Router>
      <div className="app">
        <Sidebar />
        <div className="content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/machines" element={<Machine />} />
            <Route path="/softwares" element={<Software />} />
            <Route path="/scheduled-jobs" element={<SJob />} />
            <Route path="/completed-jobs" element={<CJob />} />
            <Route path="/admin-mail" element={<Mail />} />
            <Route path="/tables" element={<Inventory />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
