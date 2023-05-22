import React from 'react'
import "./Tarif.css";
import Image1 from "../../images/boxBoulangerie.jpg";
import Image2 from "../../images/boxDecouverte.jpg";
import Image3 from "../../images/boxVinFromage.jpg";

import axios from 'axios';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Tarif() {
  const images = [Image1, Image2, Image3];
  const imagesLeft = ["-155px", "-300px", "-220px"];

  const navigate = useNavigate();

  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  function handleClick(product) {
    navigate('/AddCart/' + product);
  }

  useEffect(() => {
    const fetchData = async () => {
      const result = await axios.get('/api/data');
      setData(result.data.stocks);
      //setIsLoading(false);
    };
    fetchData();
  }, []);

  useEffect(() => {
    console.log(data)
    console.log(isLoading)
  }, []);

  return (
    <div className="Page Tarif">
        <div className="title">TARIF</div>

        <div className="container-boxs">
          {isLoading ? 
            <div>Chargement en cours...</div>
            :
            Object.keys(data).map((index, mapIndex) => (
              <div className="box">
                <div className="title-box">{data[index].name}</div>

                <div className="background-box">
                  <img style={{left:imagesLeft[mapIndex]}} src={images[mapIndex]} alt="" className="background-img" />
                  <div className="container-price">
                    <div className="price">{data[index].tarifs + ".00 €"}</div>
                  </div>
                  <div className="button-add" onClick={() => handleClick(index)}>AJOUTER AU PANIER</div>
                </div>
              </div>
            ))
          }
          
        </div> 
    </div>
  )
}

export default Tarif