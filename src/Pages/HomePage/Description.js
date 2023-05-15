import React from 'react'
import "./Description.css";
import imgDescription from "../../images/imgDescription.jpeg"

function Description() {
  return (
    <div className="Description">
        <img alt="" src={imgDescription} />
        <div className="right-part-container">
          <h1>Description</h1>
        </div>
    </div>
  )
}

export default Description