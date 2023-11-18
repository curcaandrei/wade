import React from 'react';
import AccountLogo from '../images/account.png';
import '../css/account.css';
const MyAccount=()=>{
return(
<div className="account-screen">
<div className="top-logo">
        <a href="/my-account">
          <img src={AccountLogo} alt="Logo" />
        </a>
      </div>
<div className="account-content"> 
<h1>Info about me</h1>
<div className="content-container">
<form method="post" className="contact-form">

                    <label>Full Name</label>
                    <input className="form-input" name="nameForm" placeholder="Your Name" type="text"  readOnly />
                    <label>Address</label>
                    <input className="form-input" name="addressForm" placeholder="Address" type="text" readOnly />
                    <label>Smthg else</label>
                    <input className="form-input" name="subjectForm" placeholder="Subject" type="text"  readOnly />
                </form>

    <div className="hobbies-container">
     
                <div className="hobby-card">
                    <img src='https://cdn.smehost.net/sonymusiccomau-auprod/wp-content/uploads/Havanna-Album-Artwork.jpeg'
                   />
                    <p>Title: Havana</p>
                    <p>Category: pop</p>
                </div>
        
                <div className="hobby-card">
                <img src='https://i.ebayimg.com/images/g/GtEAAOSw1W9eN1cY/s-l1600.jpg'
                   />
                    <p>Title: 1917</p>
                    <p>Category: war</p>
                </div>
      
    </div>
</div>      
</div>
</div>
);
}
export default MyAccount;