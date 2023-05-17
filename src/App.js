import React from 'react';
import './App.css';
import Header from './component/Header';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from "./Pages/Home"
import Register from "./Pages/Register"
import Login from "./Pages/Login"
import Dashboard from "./Pages/Dashboard"
import Logout from "./Pages/Logout"
import Tarif from './Pages/HomePage/Tarif';

function App() {

  return (
    <div className="App">
      <BrowserRouter>
        <Header />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/boxs" element={<Tarif />} />
        </Routes>

      </BrowserRouter>

    </div>
  );
}

export default App;
