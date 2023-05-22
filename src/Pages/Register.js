import React from 'react';
import Formulaire from '../component/Formulaire';
import "./Register.css";

function Register() {

  return (
    <div className="Register Page">
        <div className="register-page">
          <div className="title">
          <div className="the">THE</div>  
            <div className="french">FRENCH</div> 
            <div className = "flavor">FLAVOR</div>
          </div>
          <div className="login-connecter-title">S'ENREGISTRER</div>
        </div>
        <Formulaire />
    </div>
  );
}

export default Register;
