import React from 'react';
import '../css/home.css';
import MainLogo from '../images/trans2.png';
import GoogleLogo from '../images/goolr.png';
import FacebookLogo from '../images/facebook.png';
import MicrosoftLogo from '../images/microsoft.png';
import { useNavigate } from 'react-router-dom';
const HomeScreen = () => {
  const navigate = useNavigate();

  const handleLogin = () => {
    //login logiuc to be added
    navigate('./first-time-login');
  };
  const navigateMain=()=>{
    navigate('./main');
  }
  return (
    <div className="home-screen">
     
      <div className='background-image'>
      <div className="centered-logo logo-background">
        <img src={MainLogo} alt="Logo"/>
      </div>
      <div className="oauth-buttons">
        <div className="oauth-button">
        <img  className="logo-img" src={GoogleLogo} alt="google logo"/>
          <button className="login-button"  onClick={handleLogin}>Login with Google</button>
   
        </div>

        <div className="oauth-button">
        <img  className="logo-img" src={FacebookLogo} alt="facebook logo"/>
          <button className="login-button" onClick={navigateMain}>Login with Facebook</button>
        </div>
        <div className="oauth-button">
        <img className="logo-img" src={MicrosoftLogo} alt="microsoft logo"/>
          <button className="login-button">Login with Microsoft</button>
        </div>
      </div>
      </div>
    </div>
  );
}

export default HomeScreen;