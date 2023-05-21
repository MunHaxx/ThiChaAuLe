import React from 'react';
import './App.css';
import Header from './component/Header';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from "./Pages/Home"
import Login from "./Pages/Login"
import Register from "./Pages/Register"
import Tarif from './Pages/HomePage/Tarif';
import Panier from './Pages/Panier';
import Admin from './Pages/Dashboard/Admin';
import User from './Pages/Dashboard/User';

function App() {

  return (
    <div className="App">
      <BrowserRouter>
        <Header />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/boxs" element={<Tarif />} />
          <Route path="/panier" element={<Panier />} />
          <Route path="/register" element={<Register />} />
          <Route path="/admin" element={<Admin />} />
          <Route path="/userdashboard" element={<User />} />

        </Routes>

      </BrowserRouter>

    </div>
  );
}

export default App;
