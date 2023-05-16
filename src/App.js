import React from 'react';
import './App.css';
import Header from './component/Header';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from "./Pages/Home"
import Login from "./Pages/Login"
import Boxs from "./Pages/Boxs"

function App() {

  return (
    <div className="App">
      <BrowserRouter>
        <Header />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/boxs" element={<Boxs />} />
        </Routes>

      </BrowserRouter>

    </div>
  );
}

export default App;
