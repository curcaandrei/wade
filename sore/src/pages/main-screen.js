import React from 'react';
import AccountLogo from '../images/account.png';
import '../css/first-time.css';
import '../css/main-screen.css';
const MainScreen = () => {

    return (
        <div className='main-screen'>
            <div className="top-logo">
                <a href="/my-account">
                    <img src={AccountLogo} alt="Logo" />
                </a>
            </div>
            <div className='main-content' >
                <h3>Maybe you know them</h3>
                <div className='people-list'>
                    <div className='people-card purple-back'>
                        <p>sadasfsafas</p>
                    </div>
                </div>

                <section className='info-container'>
                    <div className='info-card purple-back'>
                        <p>asfasfasf</p>
                    </div>
                </section>
            </div>
        </div>

    );
}
export default MainScreen;