import React, { useState, useEffect } from 'react';
import '../css/home.css';
import MainLogo from '../images/trans2.png';
import GoogleLogo from '../images/goolr.png';
import FacebookLogo from '../images/facebook.png';
import MicrosoftLogo from '../images/microsoft.png';
import { useNavigate } from 'react-router-dom';
import { googleLogout, useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';
const HomeScreen = () => {
  const [ user, setUser ] = useState({});
  const [ profile, setProfile ] = useState([]);
  const navigate = useNavigate();

  const handleLogin = () => {
    //login logiuc to be added
    navigate('./first-time-login');
  };
  const login = useGoogleLogin({
    onSuccess: (codeResponse) => {
      console.log(codeResponse);
      setUser(codeResponse);
      console.log(codeResponse.access_token);
    },
    onError: (error) => console.log('Login Failed:', error)
});
  const errorMessage = (error) => {
    console.log(error);
};
  const navigateMain=()=>{
    navigate('/main');
  }
//   useEffect(
//     () => {
//         if (user) {
//             axios
//                 .get(`https://www.googleapis.com/oauth2/v1/userinfo?access_token=${user.access_token}`, {
//                     headers: {
//                         Authorization: `Bearer ${user.access_token}`,
//                         Accept: 'application/json'
//                     }
//                 })
//                 .then((res) => {
//                     setProfile(res.data);
//                     console.log(res.data);
//                     navigate('./first-time-login');
//                 })
//                 .catch((err) => console.log(err));
//         }
//     },
//     [ user ]
// );
useEffect(() => {
  const fetchData = async () => {
    try {
      if (Object.keys(user).length > 0) {
        const res = await axios.get(`https://www.googleapis.com/oauth2/v1/userinfo?access_token=${user.access_token}`, {
          headers: {
            Authorization: `Bearer ${user.access_token}`,
            Accept: 'application/json'
          }
        });

        setProfile(res.data);
        console.log(res.data);

        // After receiving data from Google API, make a request to localhost:5000/users/check-user
        const checkUserRes = await axios.post('https://userpf-dot-diesel-nova-412314.ew.r.appspot.com/users/check-user', res.data);
        console.log(checkUserRes );
        console.log('isknown: ' + checkUserRes.data.isKnown)
        if (checkUserRes.data.isKnown === 1) {
          navigate('/main');
        } else if (checkUserRes.data.isKnown === 0) {
          navigate('/first-time-login');
        }
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  fetchData();
}, [user, navigate]);

  return (
    <div className="home-screen">
     
      <div className='background-image'>
      <div className="centered-logo logo-background">
        <img src={MainLogo} alt="Logo"/>
      </div>
      <div className="oauth-buttons">
        <div className="oauth-button">
        <img  className="logo-img" src={GoogleLogo} alt="google logo"/>
         ' <button className="login-button"  onClick={()=>login()}>Login with Google</button>'
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