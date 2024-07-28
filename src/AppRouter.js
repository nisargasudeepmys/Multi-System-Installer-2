import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Machine from './Machine.js';
import SJob from './Scheduled-jobs.js';
import Mail from './Admin-mail.js';
import CJob from './Completed-jobs.js';
import Software from './Software.js';
import Sidebar from './Sidebar.js';
import Inventory from './Inventory.js';

function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Sidebar />} />
        <Route path="/machines" element={<Machine />} />
        <Route path="/softwares" element={<Software />} />
        <Route path="/scheduled-jobs" element={<SJob />} />
        <Route path="/completed-jobs" element={<CJob />} />
        <Route path="/admin-mail" element={<Mail />} />
        <Route path="/tables" element={<Inventory />} />
        
      </Routes>
    </Router>
  );
}

export default AppRouter;

