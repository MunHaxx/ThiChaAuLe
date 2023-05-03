import React from 'react';
import { Link } from 'react-router-dom'

function Header() {

  return (
    <div className="Header">
        <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/register">Register</Link></li>
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/dashboard">Dashboard</Link></li>
            <li><Link to="/logout">Logout</Link></li>
        </ul>
    </div>
  );
}

export default Header;
