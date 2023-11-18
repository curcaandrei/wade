import React from 'react';
import '../css/first-time.css';
import PeopleLogo from '../images/people_yell.png';
import BookLogo from '../images/book_yellow.png';
import MusicLogo from '../images/music_yeloow.png';
import MovieLogo from '../images/movie_yellow.png';
import AccountLogo from '../images/account.png';
import PersonModal from './modal-component/main-modal';
import { useState } from 'react';
const FirstTimeScreen = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };
  return (
    <div className="second-screen">
      <div className="top-logo">
        <a href="/my-account">
          <img src={AccountLogo} alt="Logo" />
        </a>
      </div>
      <div className="centered-content">
        <h1>Let's start</h1>
        <div className="search-box">
            <h4>Search for something</h4>
        </div>
        <p className="handwritten-text">Or find something that’s interesting to you</p>
        <div className="grid">
          <button className="grid-box" onClick={handleOpenModal}>
            <img src={PeopleLogo} alt="Logo 1" />
          </button>
          <div className="grid-box">
            <img src={BookLogo} alt="Logo 2" />
          </div>
          <div className="grid-box">
            <img src={MovieLogo} alt="Logo 3" />
          </div>
          <div className="grid-box">
            <img src={MusicLogo} alt="Logo 4" />
          </div>
          <PersonModal isOpen={isModalOpen} onClose={handleCloseModal} />
        </div>
      </div>
    </div>
  );
}

export default FirstTimeScreen;