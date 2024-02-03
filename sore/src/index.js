import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './appm.js'
import reportWebVitals from './reportWebVitals';
import { GoogleOAuthProvider } from "@react-oauth/google"
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <GoogleOAuthProvider clientId='199400607048-21l0godb4b3899cb1fsm5ib02c0i4ngo.apps.googleusercontent.com'>
  <React.StrictMode>
    <App />
  </React.StrictMode>
   </GoogleOAuthProvider>
);
// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
