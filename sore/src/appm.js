// App.js or wherever you manage your routes

import React from 'react';
import { Route, Routes, BrowserRouter as Router } from 'react-router-dom';
import HomeScreen from './pages/home-screen';
import FirstTimeScreen from './pages/first-time-login';
import MyAccount from './pages/my-account-screen';
import MainScreen from './pages/main-screen';
const App = () => {
  return (
    <Router>
    <Routes>
      <Route path="/" element={<HomeScreen />} />
      <Route path="/first-time-login" element={<FirstTimeScreen />} />
      <Route path="/my-account" element={<MyAccount/>} />
      <Route path='/main' element={<MainScreen/>}/>
    </Routes>
    </Router>
  );
}

export default App;