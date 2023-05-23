import React from 'react';
import { Link } from 'react-router-dom'
import './Header.css';
import imgCart from '../images/imgCart.png';
import { useState } from "react"
import { useNavigate } from 'react-router-dom';


function Header() {
  const [isOpen, setIsOpen] = useState(false);

  const navigate = useNavigate();

  const handleIsOpen = () => {
    setIsOpen(!isOpen);
  }

  const reload = () => {
    navigate("/dashboard");
    window.location.reload();
  }

  return (
    <div className={isOpen ? "Header show-header" : "Header"}>
        <div className="links" onClick={
        handleIsOpen
        }>
          <div className = "home">
            <Link to="/">HOME</Link>
            <Link to="/login">LOGIN</Link>
            <Link to="/boxs">BOXS</Link>
            <Link to="/dashboard" onClick={reload}>COMPTE</Link>
          </div>
          
          <div className="panier">
            <Link to="/panier">
              <img alt="" src={imgCart} />
              <div className="texte-panier">PANIER</div>
            </Link>
          </div>
        </div>
        <button className="burger" onClick={handleIsOpen}>
          <span className="burger-bar"></span>
        </button>
      
            
    </div>
  );
}

export default Header;
