import React, { useState, useEffect } from 'react';
import '../css/first-time.css';
import PeopleLogo from '../images/people_yell.png';
import BookLogo from '../images/book_yellow.png';
import MusicLogo from '../images/music_yeloow.png';
import MovieLogo from '../images/movie_yellow.png';
import AccountLogo from '../images/account.png';
import PersonModal from './modal-component/main-modal';
import YoutubeLogo from '../images/youtube_transp.png'
import GoodReadsLogo from '../images/png-transparent-goodreads.png';
import SpotifyLogo from '../images/Spotify_logo_without_text.svg.png';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
const FirstTimeScreen = () => {
  const userId = localStorage.getItem('user_id');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };
  const navigateMain=()=>{
    navigate('/main');
  }
  const RedirectPopOut = (url) => {
      window.open(url, '_blank');
    };
const fetchDataFromSpotify = async () => {
      try {
        setLoading(true);
        const authUrl = `https://userpf-dot-diesel-nova-412314.ew.r.appspot.com/spotify?user_id=${userId}`;
        window.location = authUrl;
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false);
      }
    };
    const fetchDataFromGoogleBooks = async () => {
      try {
        setLoading(true);
        const response=await fetch(`https://userpf-dot-diesel-nova-412314.ew.r.appspot.com/books?user_id=${userId}`);
        console.log(response);
        RedirectPopOut(response.url)
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
  return (
    <div className="second-screen">
      <div className="top-logo">
      <button type="submit" className='done-btn' onClick={navigateMain}>Next</button>
        <a href="/my-account">
          <img src={AccountLogo} alt="Logo" />
        </a>
      </div>
      <div className="centered-content">
        <h1>Let's start</h1>
        <div className="search-box">
            <h4>Search for something</h4>
            {loading ? (
          <p>Loading...</p>
        ) : (
          <p></p>
        )}
        </div>
        <p className="handwritten-text">Or find something that’s interesting to you</p>
        <div className="grid">
          <button className="grid-box" onClick={handleOpenModal}>
            <img src={PeopleLogo} alt="Logo people" />
          </button>
          <div className="grid-box">
            <img src={BookLogo} alt="Logo books" />
          </div>
          <div className="grid-box">
            <img src={MovieLogo} alt="Logo movie" />
          </div>
          <div className="grid-box">
            <img src={MusicLogo} alt="Logo music" />
          </div>
          <PersonModal isOpen={isModalOpen} onClose={handleCloseModal} />
        </div>
        <div className="grid top-space">
          <div className="grid-box">
            <img src={YoutubeLogo} alt="Logo youtube"/>
          </div>
          <div className="grid-box">
            <img src={GoodReadsLogo} alt="Logo goodreads" onClick={fetchDataFromGoogleBooks} />
          </div>
          <div className="grid-box">
            <img src={SpotifyLogo} alt="Logo spotify" onClick={fetchDataFromSpotify}/>
          </div>
        </div>
      </div>
    </div>
  );
}

export default FirstTimeScreen;