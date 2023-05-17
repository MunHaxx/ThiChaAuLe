import React from 'react';
import "./Contact.css";
import imgContact from "../../images/imgContact.jpg";

function Contact() {
  return (
    <div className="Contact">
        <div className="container">
          <div className='contact-img-container'><img className='contact-img' alt="" src={imgContact} /></div>
          <div className="information-container">
            <div className="contact-info-title">À BIENTÔT !</div>
            <div className="contact-info">
              <div className="info-title">NUMÉRO DE TÉLÉPHONE</div>
              <div className="info">01 23 45 67 78</div>
              <div className="info-title">ADRESSE E-MAIL</div>
              <div className="info">jesuistropdouéendesign@gmail.com</div>
              <div className="info-title">SIÈGE SOCIAL</div>
              <div className="info">12 rue Desaix, 97200 Fort de France</div>
            </div>
          </div>
        </div>
    </div>
  )
}

export default Contact