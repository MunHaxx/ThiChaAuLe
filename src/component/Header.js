import React from 'react';
import { Link } from 'react-router-dom'
import './Header.css';
import imgCart from '../images/imgCart.png';

function Header() {

  return (
    <div className="Header">
        <div className = "container">
            <div className = "home">
              <Link to="/">HOME</Link>
              <Link to="/login">LOGIN</Link>
              <Link to="/boxs">BOXS</Link>
            </div>
            
            <div className = "panier">
              <Link to="/panier">
                <img alt="" src = {imgCart}/>
                PANIER
              </Link>
            </div>
            
        </div>
    </div>
  );
}

export default Header;
