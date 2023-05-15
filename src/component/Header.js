import React from 'react';
import { Link } from 'react-router-dom'
import './Header.css';

function Header() {

  return (
    <div className="Header">
        <div className = "container">
            <div className = "home">
              <Link to="/">HOME</Link>
              <Link to="/login">LOGIN</Link>
              <Link to="/boxs">BOXS</Link>
            </div>
            <div className = "panier"><Link to="/panier">PANIER</Link></div>
        </div>
    </div>
  );
}

export default Header;
