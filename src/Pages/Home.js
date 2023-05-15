import React from 'react';
import "./Home.css";
import Bienvenue from './HomePage/Bienvenue'
import Description from './HomePage/Description'
import Tarif from './HomePage/Tarif'
import Temoignages from './HomePage/Temoignages'
import Contact from './HomePage/Contact'

function Home() {
  return (
    <div className="Home">
      <Bienvenue />
      <Description />
      <Tarif />
      <Temoignages />
      <Contact />
    </div>
  );
}

export default Home;
