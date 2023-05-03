import React from "react";


function Formulaire() {

    return (
      <div className="containerFormulaire">
        <h1>Formulaire</h1>

        <div className="inputContainer">
          <form method="post">
            <input id="id" type="text" name="id" placeholder="ID"/>
            <input id="password" type="password" name="password" placeholder="Password"/>
            <button type="submit" value="valider">Valider</button>
          </form>
        </div>
      </div>
    );
  }
  
  export default Formulaire;
  