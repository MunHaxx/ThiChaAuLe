import './App.css';

function App() {

  return (
    <div className="App">
      {/* <div>My name is Noah</div> */}
      <div className="bonjour">Bonjour à tous</div>
      <div className="containerBulbizarre">
        <div className='carréDansLaxe'>
          <img alt="" className="bulbizarre" src='https://www.pokepedia.fr/images/thumb/e/ef/Bulbizarre-RFVF.png/250px-Bulbizarre-RFVF.png' />
        </div>

        <div className="descriptionBulbizarre">
          <h1>Bulbizarre</h1>
          <p>Bulbizarre est un pokémon de la première gen de type plante</p>
        </div>
      </div>
      <a href="https://eu.shop.battle.net/fr-fr">Battle net</a>
      
    </div>
  );
}

export default App;
