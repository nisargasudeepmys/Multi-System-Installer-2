import React from 'react';
import { Link } from 'react-router-dom';
import { FaCalendarAlt, FaUser,  FaDatabase,  FaBook, FaHome } from 'react-icons/fa';
import './Sidebar.css';
import { MdOutlineTaskAlt } from "react-icons/md";

const Sidebar = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>Multi System Installer</h2>
      </div>
      <ul className="sidebar-menu">
      <li>
          <Link to="/">
            <FaHome />
            <span>Home</span>
          </Link>
        </li>
        <li>
          <Link to="/machines">
            <FaDatabase />
            <span>Machines</span>
          </Link>
        </li>
        <li>
          <Link to="/softwares">
            <FaDatabase />
            <span>Softwares</span>
          </Link>
        </li>
        <li>
          <Link to="/scheduled-jobs">
            <FaCalendarAlt />
            <span>Scheduled Jobs</span>
          </Link>
        </li>
        <li>
          <Link to="/completed-jobs">
            <MdOutlineTaskAlt />
            <span>Completed Jobs</span>
          </Link>
        </li>
        <li>
          <Link to="/admin-mail">
            <FaUser />
            <span>Account</span>
          </Link>
        </li>
        <li>
          <Link to="/tables">
            <FaBook />
            <span>Software Inventory</span>
          </Link>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
