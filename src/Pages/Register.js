import React from 'react';
import Formulaire from '../component/Formulaire';
import "./Register.css";

function Register() {

  return (
    <div className="Register">
        <div className="register-page">
          <div className="login-site-title">
            <span className="the">THE</span>  
            <span className="french">FRENCH</span> 
            <span className = "flavor">FLAVOR</span>
          </div>
          <div className="login-connecter-title">S'ENREGISTRER</div>
        </div>
        <Formulaire />
    </div>
  );
}

export default Register;
